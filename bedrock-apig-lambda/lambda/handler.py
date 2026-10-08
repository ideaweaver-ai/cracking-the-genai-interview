"""API Gateway → Lambda → Amazon Bedrock Mantle (OpenAI Responses API) Q&A handler.

Uses bedrock-mantle only (not bedrock-runtime / Converse).
Default model: xai.grok-4.6 (us-west-2)

Requires the `openai` package in the deployment package (see README / scripts/package-lambda.sh).
Docs: https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html
"""

from __future__ import annotations

import base64
import json
import logging
import os
from typing import Any

from aws_bedrock_token_generator import provide_token
from openai import OpenAI

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEFAULT_MODEL_ID = "xai.grok-4.6"
# Grok spends many tokens on reasoning; 1024 is often too low and yields empty answers.
DEFAULT_MAX_TOKENS = "4096"
DEFAULT_REGION = "us-west-2"
DEFAULT_MANTLE_API_PATH = "/openai/v1"
DEFAULT_REASONING_EFFORT = "low"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST",
    "Content-Type": "application/json",
}


def _response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body),
    }


def _parse_body(event: dict[str, Any]) -> dict[str, Any]:
    body = event.get("body")
    if body is None:
        return {}
    if isinstance(body, dict):
        return body
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    if isinstance(body, str):
        body = body.strip()
        if not body:
            return {}
        return json.loads(body)
    return {}


def _mantle_api_path() -> str:
    path = os.environ.get("MANTLE_API_PATH", DEFAULT_MANTLE_API_PATH).strip()
    if not path.startswith("/"):
        path = "/" + path
    return path.rstrip("/") or "/v1"


def _mantle_base_url(region: str) -> str:
    return f"https://bedrock-mantle.{region}.api.aws{_mantle_api_path()}"


def _mantle_region() -> str:
    return (
        os.environ.get("BEDROCK_REGION")
        or os.environ.get("AWS_REGION")
        or DEFAULT_REGION
    )


def _bedrock_api_key() -> str:
    """Prefer a short-term token from the Lambda IAM role (recommended)."""
    use_static = os.environ.get("USE_STATIC_BEDROCK_API_KEY", "").lower() in (
        "1",
        "true",
        "yes",
    )
    static = (
        os.environ.get("BEDROCK_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()
    if use_static and static:
        return static
    return provide_token(region=_mantle_region())


def _extract_answer(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text

    chunks: list[str] = []
    for item in getattr(response, "output", None) or []:
        item_type = getattr(item, "type", None)
        if item_type != "message":
            continue
        for part in getattr(item, "content", None) or []:
            if getattr(part, "type", None) in ("output_text", "text"):
                part_text = getattr(part, "text", None)
                if part_text:
                    chunks.append(part_text)
    return "".join(chunks)


def _create_mantle_client() -> OpenAI:
    region = _mantle_region()
    return OpenAI(
        api_key=_bedrock_api_key(),
        base_url=_mantle_base_url(region),
    )


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    http_method = (
        event.get("httpMethod")
        or event.get("requestContext", {}).get("http", {}).get("method")
        or ""
    )
    if http_method.upper() == "OPTIONS":
        return _response(200, {"message": "ok"})

    try:
        payload = _parse_body(event)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        logger.warning("Invalid JSON body: %s", exc)
        return _response(400, {"error": "Request body must be valid JSON"})

    question = (payload.get("question") or payload.get("prompt") or "").strip()
    if not question:
        return _response(
            400,
            {"error": "Missing required field: question (or prompt)"},
        )

    model_id = os.environ.get("MODEL_ID", DEFAULT_MODEL_ID)
    max_tokens = int(os.environ.get("MAX_TOKENS", DEFAULT_MAX_TOKENS))
    reasoning_effort = os.environ.get(
        "REASONING_EFFORT", DEFAULT_REASONING_EFFORT
    ).strip() or DEFAULT_REASONING_EFFORT

    create_kwargs: dict[str, Any] = {
        "model": model_id,
        "input": [{"role": "user", "content": question}],
        "max_output_tokens": max_tokens,
    }
    # Grok (and similar) always reason; without enough tokens / low effort,
    # responses often finish as status=incomplete with an empty message.
    if reasoning_effort.lower() not in ("", "none", "off"):
        create_kwargs["reasoning"] = {"effort": reasoning_effort}

    try:
        client = _create_mantle_client()
        mantle_response = client.responses.create(**create_kwargs)
    except RuntimeError as exc:
        logger.error("%s", exc)
        return _response(500, {"error": str(exc)})
    except Exception as exc:
        logger.exception("Bedrock Mantle Responses API failed")
        return _response(
            500,
            {
                "error": "Failed to get a response from Bedrock Mantle",
                "detail": type(exc).__name__,
            },
        )

    answer = _extract_answer(mantle_response)
    if not answer:
        status = getattr(mantle_response, "status", None)
        usage = getattr(mantle_response, "usage", None)
        logger.warning(
            "Mantle returned no text content (status=%s usage=%s): %s",
            status,
            usage,
            mantle_response,
        )
        detail = (
            "Model used its token budget on reasoning before producing an answer. "
            "Increase MAX_TOKENS or set REASONING_EFFORT=low."
            if status == "incomplete"
            else "Model returned an empty answer"
        )
        return _response(500, {"error": detail, "status": status})

    return _response(
        200,
        {
            "answer": answer,
            "model": model_id,
            "endpoint": "bedrock-mantle",
        },
    )

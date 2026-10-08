#!/usr/bin/env bash
# Build a Linux-compatible lambda/function.zip (handler + openai deps).
#
# IMPORTANT: Do NOT use a plain `pip install -t` on macOS/Windows.
# pydantic_core ships native .so files — Lambda needs manylinux wheels.
#
# Usage (from repo root):
#   ./scripts/package-lambda.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LAMBDA_DIR="$ROOT/lambda"
PACKAGE_DIR="$LAMBDA_DIR/package"
ZIP_PATH="$LAMBDA_DIR/function.zip"
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"

rm -rf "$PACKAGE_DIR" "$ZIP_PATH"
mkdir -p "$PACKAGE_DIR"

echo "Installing Linux (manylinux) wheels for Lambda Python ${PYTHON_VERSION} ..."
python3 -m pip install \
  -r "$LAMBDA_DIR/requirements.txt" \
  -t "$PACKAGE_DIR" \
  --upgrade \
  --only-binary=:all: \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version "$PYTHON_VERSION" \
  --quiet

# Console default handler module name
cp "$LAMBDA_DIR/handler.py" "$PACKAGE_DIR/lambda_function.py"

# Sanity check: Linux native pydantic_core extension must be present
if ! find "$PACKAGE_DIR" -name '_pydantic_core*.so' | grep -q .; then
  echo "ERROR: No Linux _pydantic_core*.so found in package/."
  echo "pip may have fallen back to incompatible wheels. Aborting."
  exit 1
fi

echo "Creating zip at package root ..."
(
  cd "$PACKAGE_DIR"
  zip -r "$ZIP_PATH" . -q
)

echo
echo "Created: $ZIP_PATH"
ls -lh "$ZIP_PATH"
echo
echo "Upload in AWS Console (us-west-2):"
echo "  Code → Upload from → .zip file → select function.zip → Save"
echo "  Handler: lambda_function.lambda_handler"
echo "  Also set Memory to at least 256 MB (Configuration → General)."

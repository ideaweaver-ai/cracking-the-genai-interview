import requests

WEBHOOK_ENDPOINT = ""  # webhook-test works only while "Execute workflow" is active

question = "What is GenAI and how it works?"

body = {"message": question, "sessionId": "test-session-1"}

result = requests.post(WEBHOOK_ENDPOINT, json=body, timeout=120)

print("Status:", result.status_code)

print(result.text)

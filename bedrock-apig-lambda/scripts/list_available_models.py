
from openai import OpenAI
from tabulate import tabulate

client = OpenAI(
    base_url="https://bedrock-mantle.us-west-2.api.aws/v1",
    api_key="<your-api-key>",
    default_headers={"OpenAI-Project": "default"},
)

models = client.models.list()

table = []

for model in sorted(models.data, key=lambda m: m.id):
    provider = model.id.split(".")[0].upper()

    table.append([
        provider,
        model.id,
        model.status
    ])

print(tabulate(
    table,
    headers=["Provider", "Model ID", "Status"],
    tablefmt="grid"
))

print(f"\nTotal Models: {len(table)}")

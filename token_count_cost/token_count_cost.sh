#!/bin/bash

# ==============================
# Configuration
# ==============================

API_KEY=""
MODEL="gpt-5"
PROMPT="Explain DevOps in simple terms"

# Pricing per 1K tokens (update based on actual model pricing)
INPUT_PRICE_PER_1K=0.01
OUTPUT_PRICE_PER_1K=0.03

# ==============================
# API Call
# ==============================

response=$(curl -s https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
    \"model\": \"$MODEL\",
    \"input\": \"$PROMPT\"
  }")

# ==============================
# Extract Token Usage
# ==============================

input_tokens=$(echo "$response" | jq '.usage.input_tokens')
output_tokens=$(echo "$response" | jq '.usage.output_tokens')
total_tokens=$(echo "$response" | jq '.usage.total_tokens')

# ==============================
# Cost Calculation
# ==============================

input_cost=$(echo "scale=6; ($input_tokens / 1000) * $INPUT_PRICE_PER_1K" | bc)
output_cost=$(echo "scale=6; ($output_tokens / 1000) * $OUTPUT_PRICE_PER_1K" | bc)
total_cost=$(echo "scale=6; $input_cost + $output_cost" | bc)

# ==============================
# Output
# ==============================

echo "=============================="
echo "Model: $MODEL"
echo "Input Tokens: $input_tokens"
echo "Output Tokens: $output_tokens"
echo "Total Tokens: $total_tokens"
echo "------------------------------"
echo "Input Cost:  \$$input_cost"
echo "Output Cost: \$$output_cost"
echo "Total Cost:  \$$total_cost"
echo "=============================="

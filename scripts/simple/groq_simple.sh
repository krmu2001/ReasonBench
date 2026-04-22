#!/bin/bash

benchmark="judgelm"
method="io"
split="single"

provider="groq"
api_key="GROQ_API_KEY"

# Free tier limits:
#   TPM - 6K
#   TPD - 500K
model="llama-3.1-8b-instant"

# Free tier limits:
#   TPM - 12K
#   TPD - 100K
# model="llama-3.3-70b-versatile"

# Decoding parameters
source scripts/configs/$benchmark.env

# Override MAX_COMPLETION_TOKENS if method is "io" or "cot"
if [[ "$method" == "io" || "$method" == "cot" ]]; then
  MAX_COMPLETION_TOKENS=3000
fi

python scripts/simple/simple.py \
    --benchmark "$benchmark" \
    --method "$method" \
    --model "$model" \
    --batch_size 1 \
    --timeout 2.0 \
    --temperature "$TEMPERATURE" \
    --max_completion_tokens "$MAX_COMPLETION_TOKENS" \
    --top_p "$TOP_P" \
    --dataset_path "datasets/dataset_${benchmark}.jsonl" \
    --split "$split" \
    --correctness 1 \
    --allow_batch_overflow 1 \
    --ns_ratio 0.0 \
    --provider "$provider" \
    --api_key "$api_key" \
    ${STOP:+--stop "$STOP"} \
    --value_cache

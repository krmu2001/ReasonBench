#!/bin/bash

set -euo pipefail

benchmark="judgelm"
method="io"
split="single"
provider="groq"
api_key="GROQ_API_KEY"
model="llama-3.1-8b-instant"
cache_path="caches/judgelm"
dataset_path="datasets/dataset_${benchmark}.jsonl"

batch_size=1
timeout=2.0
allow_batch_overflow=1
ns_ratio=0.0
correctness=1
use_value_cache=1

clean_cache=0
archive_logs=0


timestamp="$(date +%Y%m%d_%H%M%S)"
run_name=""

usage() {
  cat <<EOF
Usage: $0 [options]

Options:
  --method <name>               Method to run (default: io)
  --split <name>                Dataset split (default: single)
  --model <name>                Model name
  --provider <name>             Provider (default: groq)
  --dataset-path <path>         Dataset path
  --cache-path <path>           Cache path
  --run-name <name>             Explicit run name
  --clean-cache                 Remove cache directory before run
  --no-value-cache              Disable method internal cache
  --archive-logs                Archive existing logs
  -h, --help                    Show this help

EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --method) method="$2"; shift 2 ;;
    --split) split="$2"; shift 2 ;;
    --model) model="$2"; shift 2 ;;
    --provider) provider="$2"; shift 2 ;;
    --dataset-path) dataset_path="$2"; shift 2 ;;
    --cache-path) cache_path="$2"; shift 2 ;;
    --run-name) run_name="$2"; shift 2 ;;
    --clean-cache) clean_cache=1; shift ;;
    --no-value-cache) use_value_cache=0; shift ;;
    --archive-logs) archive_logs=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done


source "scripts/configs/${benchmark}.env"

if [[ "method" == "io" || "$method" == "cot" ]]; then
  MAX_COMPLETION_TOKENS=3000
fi

if [[ -z "$run_name" ]]; then
  run_name="${timestamp}_${benchmark}_${method}_${split}_${model//\//-}"
fi

# Logging layout
framework_log_dir="logs/${benchmark}/framework"
raw_calls_log_dir="logs/${benchmark}/raw_calls"
mkdir -p "$framework_log_dir"
mkdir -p "$raw_calls_log_dir"

framework_log_name="framework_${run_name}.log"
raw_calls_log_name="raw_${run_name}.log"

framework_log_path="${framework_log_dir}/${framework_log_name}"
raw_calls_log_path="${raw_calls_log_dir}/${raw_calls_log_name}"

archive_dir="logs/archive/${run_name}/${benchmark}"
archive_framework_dir="${archive_dir}/framework"
archive_raw_calls_dir="${archive_dir}/raw_calls"

if [[ "$archive_logs" -eq 1 ]]; then
  mkdir -p "$archive_framework_dir" "$archive_raw_calls_dir"
  # "$archive_stdout_dir"

  shopt -s nullglob

  for f in "${framework_log_dir}"/*.log; do
    mv "$f" "$archive_framework_dir/"
  done

  for f in "${raw_calls_log_dir}"/*.log; do
    mv "$f" "$archive_raw_calls_dir/"
  done

  shopt -u nullglob
fi


if [[ "$clean_cache" -eq 1 ]]; then
  echo "Removing cache at: ${cache_path}"
  rm -rf "$cache_path"
fi

mkdir -p "$(dirname "$cache_path")"

cmd=(
  python scripts/simple/simple.py
  --benchmark "$benchmark"
  --method "$method"
  --model "$model"
  --batch_size "$batch_size"
  --timeout "$timeout"
  --temperature "$TEMPERATURE"
  --max_completion_tokens "$MAX_COMPLETION_TOKENS"
  --top_p "$TOP_P"
  --dataset_path "$dataset_path"
  --split "$split"
  --correctness "$correctness"
  --allow_batch_overflow "$allow_batch_overflow"
  --ns_ratio "$ns_ratio"
  --provider "$provider"
  --api_key "$api_key"
  --framework_log_path "$framework_log_path"
  --raw_calls_log_path "$raw_calls_log_path"
  --cache_path "$cache_path"
)

if [[ -n "${STOP:-}" ]]; then
  cmd+=(--stop "$STOP")
fi

if [[ "$use_value_cache" -eq 1 ]]; then
  cmd+=(--value_cache)
fi

echo "Run name:     $run_name"
echo "Dataset path: $dataset_path"
echo "Cache path:   $cache_path"
echo "Running:"
printf ' %q' "${cmd[@]}"
echo
echo

"${cmd[@]}"

echo
echo "Run complete."
echo "Framework log path:     $framework_log_path"
echo "Raw calls log path:     $raw_calls_log_path"
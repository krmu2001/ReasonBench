import os
import time
import asyncio
import argparse

from diskcache import Cache
from omegaconf import OmegaConf

import logging
logger = logging.getLogger(__name__)

from cachesaver.pipelines import OnlineAPI

import sys
sys.path.append(os.getcwd())

from reasonbench import BenchmarkFactory, EnvironmentFactory, MethodFactory
from reasonbench.tasks import *
from reasonbench.methods import *
from reasonbench.models import OnlineLLM, API
from reasonbench.typedefs import DecodingParameters

from reasonbench.utils import initial_logging, final_logging

# Cache directory
os.makedirs(os.path.dirname(cache_path), exist_ok=True)
cache = Cache(cache_path)

model = OnlineLLM(provider=args.provider, api_key=args.api_key, reasoning_effort=args.reasoning_effort)

# Pipeline
pipeline = OnlineAPI(
    model=model,
    cache=cache,
    batch_size=args.batch_size,
    timeout=args.timeout,
    allow_batch_overflow=args.allow_batch_overflow,
    correctness=bool(args.correctness)
)

# API
api = API(
    pipeline=pipeline,
    model=args.model,
    log_path=f"logs/raw_calls/simple/{args.model}/{args.benchmark}/{args.method}_{args.split}.log"
)


response = await api.complete(
    messages=[{"role": "user", "content": "hvad er 2+2"}],
    decoding_params=params
)

print(response)
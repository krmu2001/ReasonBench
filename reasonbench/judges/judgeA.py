import os
import asyncio
from typing import Counter

from diskcache import Cache

from cachesaver.pipelines import OnlineAPI
from dotenv import load_dotenv

from reasonbench.models import OnlineLLM, API
from reasonbench.typedefs import DecodingParameters

load_dotenv()

async def judge_a(api, params, prompt, repeats=10, namespace="judgeA"):
    answers = []

    for i in range(repeats):
        request_id = f"idx0-judgeA-{i}"
        answer = await api.request(
            prompt=prompt,
            n=1,
            request_id=request_id,
            namespace=namespace,
            params=params
        )
        answers.append(answer)

    counts = Counter(answers)
    majority_answer, majority_count = counts.most_common(1)[0]

    return {
        "prompt": prompt,
        "answers": answers,
        "counts": dict(counts),
        "majority_answer": majority_answer,
        "majority_count": majority_count,
        "repeats": repeats
    }
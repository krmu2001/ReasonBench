import os
import asyncio
from diskcache import Cache

from cachesaver.pipelines import OnlineAPI
from dotenv import load_dotenv

from reasonbench.judges.judgeA import judge_a
from reasonbench.models import OnlineLLM, API
from reasonbench.typedefs import DecodingParameters

load_dotenv()


async def main():
    # ---- Hardcoded config ----
    cache_path = "caches/dev"
    provider = "groq"
    api_key = "GROQ_API_KEY"
    model_name = "llama-3.1-8b-instant"
    model_name2 = "llama-3.3-70b-versatile"

    print("API key loaded:", bool(os.getenv(api_key)))
    # ---- Cache ----
    os.makedirs(cache_path, exist_ok=True)
    cache = Cache(cache_path)

    # ---- Model ----
    model = OnlineLLM(
        provider=provider,
        api_key=api_key,
        reasoning_effort=None
    )

    # ---- Pipeline ----
    pipeline = OnlineAPI(
        model=model,
        cache=cache,
        batch_size=1,
        timeout=30,
        allow_batch_overflow=True,
        correctness=False
    )

    # ---- API wrapper ----
    api = API(
        pipeline=pipeline,
        model=model_name,
        log_path="logs/test.log"
    )

    api2 = API(
        pipeline=pipeline,
        model=model_name2,
        log_path="logs/test.log"
    )

    # ---- Decoding params ----
    params = DecodingParameters(
        temperature=0.0,
        max_completion_tokens=50,
        top_p=1.0,
        stop=None,
        logprobs=False
    )

    def outputResult(result):
        print("Prompt:", result["prompt"])
        print("Answers:", result["answers"])
        print("Counts:", result["counts"])
        print("Majority answer:", result["majority_answer"])
        print("Majority count:", result["majority_count"])
        print("Repeats:", result["repeats"])


    # JUDGE A
    result = await judge_a(api, params,"What is a good color for a car? Answer with one word.",10)
    result2 = await judge_a(api2, params,"What is a good color for a car? Answer with one word.",10)
    outputResult(result)
    print("======"*15)
    outputResult(result2)


if __name__ == "__main__":
    asyncio.run(main())





    # response = await api.request(
    #     prompt="explain what google is",
    #     n=1,
    #     request_id="idx0-test",
    #     namespace="test",
    #     params=params
    # )
    #
    # print("Response:", response)

    # # ---- CALL ----
    # async def ask_llm(prompt, n=1, request_id="idx0-ask", namespace="default"):
    #     response = await api.request(
    #         prompt=prompt,
    #         n=n,
    #         request_id=request_id,
    #         namespace=namespace,
    #         params=params
    #     )
    #     return response
    #
    #
    #
    #
    # response = await ask_llm("explain 2+2 * 3")
    #
    # print(response)
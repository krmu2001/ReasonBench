import os
import asyncio
from diskcache import Cache

from cachesaver.pipelines import OnlineAPI
from dotenv import load_dotenv

from reasonbench.judges.judgeA import JudgeA
from reasonbench.judges.judgeB import JudgeB
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
    model_name3 = "openai/gpt-oss-20b"

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
    api1 = API(
        pipeline=pipeline,
        model=model_name,
        log_path="logs/test.log"
    )

    api2 = API(
        pipeline=pipeline,
        model=model_name2,
        log_path="logs/test.log"
    )

    api3 = API(
        pipeline=pipeline,
        model=model_name3,
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

    def outputResultJudgeA(result):
        print("Prompt:", result["prompt"])
        print("Answers:", result["answers"])
        print("Counts:", result["counts"])
        print("Majority answer:", result["majority_answer"])
        print("Majority count:", result["majority_count"])
        print("Repeats:", result["repeats"])

    def outputResultJudgeB(result):
        print("Prompt:", result["prompt"])
        print("Answers:", result["answers"])
        print("Answers by Judge:", result["answers_by_judge"])
        print("Judges:", result["judges"])
        print("Repeats:", result["repeats"])


    # JUDGE A
    judge1 = JudgeA(api1,params,10)
    judge2 = JudgeA(api2,params,10)

    apis = [api1, api2, api3]
    # JUDGE B
    judge3 = JudgeB(
        api=api1,
        params=params,
        repeats=5
    )

    questionForA = "What is a good color for a car? Answer with one word."
    questionForB = "What is a good color for a car? Answer with one word."
    #
    # result1 = await judge1.solve(questionForA)
    # result2 = await judge2.solve(questionForA)
    result3 = await judge3.solve(questionForB)
    # outputResultJudgeA(result1)
    # print("======"*15)
    # outputResultJudgeA(result2)
    # print("======"*15)
    outputResultJudgeB(result3)


if __name__ == "__main__":
    asyncio.run(main())
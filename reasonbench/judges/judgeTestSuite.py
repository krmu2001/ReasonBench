import os
import asyncio
from diskcache import Cache

from cachesaver.pipelines import OnlineAPI
from dotenv import load_dotenv

from reasonbench.models import OnlineLLM, API
from reasonbench.typedefs import DecodingParameters

load_dotenv()


async def main():
    # ---- Hardcoded config ----
    #print(os.getenv("GROQ_API_KEY"))
    cache_path = "caches/dev"
    provider = "groq"  # eller "groq"
    api_key = "GROQ_API_KEY"
    model_name = "llama-3.1-8b-instant"  # eller groq model

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

    # ---- Decoding params ----
    params = DecodingParameters(
        temperature=0.0,
        max_completion_tokens=50,
        top_p=1.0,
        stop=None,
        logprobs=False
    )

    # ---- CALL ----
    async def ask_llm(prompt, n=1, request_id="idx0-ask", namespace="default"):
        response = await api.request(
            prompt=prompt,
            n=n,
            request_id=request_id,
            namespace=namespace,
            params=params
        )
        return response



    response = await ask_llm("explain 2+2 * 3")

    print(response)


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
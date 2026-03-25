import os
import asyncio
from diskcache import Cache

from cachesaver.pipelines import OnlineAPI
from dotenv import load_dotenv

from reasonbench.models import OnlineLLM, API
from reasonbench.typedefs import DecodingParameters

load_dotenv()




def counter():
    return 0

# import random
# import logging
# import asyncio
# from typing import TypedDict
# from collections import Counter
# from omegaconf import OmegaConf
# from ..typedefs import Method, Model, Agent, Environment, DecodingParameters, State, Benchmark, MAX_SEED
# from .. import MethodFactory, AgentDictFactory
# from ..utils import Resampler
# logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

load_dotenv()


#client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=os.getenv("OPENAI_API_KEY_CLAN"), timeout=300, max_retries=1)

groq_ins = os.getenv("LLM_1")
groq_ver = os.getenv("LLM_2")

#print(groq_ins, groq_ver)
client = Groq(
    api_key=os.environ.get("OPENAI_API_KEY_CLAN"),
)

def get_llm_response(model, query, temperature=0.0):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": query}
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

print(get_llm_response(groq_ins, "What is 2+2"))

print("=="*30)
print(get_llm_response(groq_ver, "Explain 2 * 3"))

#####
#### This code need to be set up the signature from reasonbench
####
#####
# @AgentDictFactory.register
# class AgentDictCoT(TypedDict):
#     step: Agent # ActAgent
#     step_params: DecodingParameters
#
#
# @MethodFactory.register
# class MethodCOT_SC(Method):
#     def __init__(self,
#                  model: Model,
#                  agents: AgentDictCoT,
#                  env: Environment,
#                  config: OmegaConf,
#                  ):
#         super().__init__(model, agents, env, config)
#
#         self.step_agent = agents["step"]
#         self.step_params = agents["step_params"]
#
#         self.n = config.n
#         assert self.n > 1, "CoT-SC needs at least 2 outputs"




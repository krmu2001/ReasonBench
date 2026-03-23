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
import sys
from typing import Counter

from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

load_dotenv()


#client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=os.getenv("OPENAI_API_KEY_CLAN"), timeout=300, max_retries=1)

groq_ins = os.getenv("LLM_1")
groq_ver = os.getenv("LLM_2")

missing_in_env = []

if groq_ins is None:
    missing_in_env.append("LLM_1")

if groq_ver is None:
    missing_in_env.append("LLM_2")


if missing_in_env:
    print(f"Missing environment variables: {', '.join(missing_in_env)}")
    sys.exit(1)


#print(groq_ins, groq_ver)
client = Groq(
    api_key=os.environ.get("OPENAI_API_KEY_CLAN"),
)

def get_llm_response(model, query, sysquery=None, temperature=1.2):
    messageQuery = []

    if sysquery is not None:
        messageQuery.append({
            "role": "system",
            "content": sysquery
        })
    messageQuery.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=model,
        messages=messageQuery,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()



def evalquerys(amountOfTimes,query):
    answers = []
    for i in range(amountOfTimes): # 0 to 4 when typing 5
        answers.append( get_llm_response(groq_ins, query))
        answers.append(get_llm_response(groq_ver, query))
    return answers



def judgeA(answer):
    counts = Counter(answer)
    most_common = counts.most_common(1)[0][0]
    return most_common

##JUDGE A
eval_answers = evalquerys(10, "What color should a car be? Answer with only one color.")
# print("Eval" + "="*30)
#print(eval_answers)
# print("JudgeEval" + "="*30)
# print(judgeA(eval_answers))
##JUDGE A END
## JUDGE C
answers_str = ", ".join(eval_answers)
print(answers_str)
print("=="*30)
print(get_llm_response(groq_ins, f"Answers: {answers_str}","You are a judge what do you think the correct answer is, and why?, the question is: What color should a car be? Answer with only one color. "))

## JUDGE C END


# print(get_llm_response(groq_ins, "What is 2+2"))
# print("=="*30)
# print(get_llm_response(groq_ver, "What is 2 * 3"))
# print("=="*30)
# print(get_llm_response(groq_ver, "What is 2 * 3", "You are a math teacher"))


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
#                  nv: Environment,
#                  config: OmegaConf,
#                  ):
#         super().__init__(model, agents, env, config)
#
#         self.step_agent = agents["step"]
#         self.step_params = agents["step_params"]
#
#         self.n = config.n
#         assert self.n > 1, "CoT-SC needs at least 2 outputs"




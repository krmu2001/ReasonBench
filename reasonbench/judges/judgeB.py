import os
from typing import Tuple, List, Dict

from dotenv import load_dotenv
from reasonbench.typedefs import Judge

load_dotenv()

class JudgeB(Judge):
    def __init__(self,
                 apis: List,
                 params,
                 repeats=10,
                 judges=None,
                 namespace="judgeB"
    ):
        self.apis = apis
        self.params = params
        self.repeats = repeats
        if judges is None:
            judges = [
                os.getenv("LLM_1"),
                os.getenv("LLM_2"),
                os.getenv("LLM_3"),
            ]
        self.judges = judges
        self.namespace = namespace

    async def eval(self, prompt, request_id, api):
        response = await api.request(
            prompt = prompt,
            n = 1,
            request_id = request_id,
            namespace = self.namespace,
            params = self.params,
        )
        return response

    async def solve(self, prompt):
        answers = []
        answers_by_judge = {}

        for judge, api in enumerate(self.apis):
            judge_name = api.model
            answers_by_judge[judge_name] = []

            for i in range(self.repeats):
                request_id = f"idx0-judgeB--{judge}-{i}"
                response = await self.eval(prompt, request_id, api=api)
                answers.append(response)
                answers_by_judge[judge_name].append(response)

        return {
            "prompt": prompt,
            "answers": answers,
            "answers_by_judge": answers_by_judge,
            "judges": [api.model for api in self.apis],
            "repeats": self.repeats
        }
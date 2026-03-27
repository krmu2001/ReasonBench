import os
from typing import Tuple, List, Dict

from dotenv import load_dotenv
from reasonbench.typedefs import Judge

load_dotenv()

class JudgeB(Judge):
    def __init__(self, api, params, repeats=10, judges=None, namespace="judgeB"):
        self.api = api
        self.params = params
        self.repeats = repeats
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

    async def eval_amount(self, amount, prompt):
        answers = []
        for i in range(amount):
            request_id = f"idx0-judgeB-{i}"
            answer = await self.eval(prompt, request_id,self.api)
            answers.append(answer)
        return answers


    async def multiple_judges(self, prompt, apis: List):
        responses = self.eval_amount(10, prompt)
        res_tostring = "".join(responses)
        dif_judges = []
        for i in range(apis.__sizeof__()):
            request_id = f"idx0-judgeB-apis-{i}"
            answer = await self.eval(res_tostring, request_id, apis[i])
            dif_judges.append(answer)

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
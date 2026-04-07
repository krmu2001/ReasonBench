import os
from typing import Tuple, List, Dict

from dotenv import load_dotenv
from reasonbench.typedefs import Judge

load_dotenv()

class JudgeB(Judge):
    def __init__(self, api, params,api_list, repeats=10, judges=None, namespace="judgeB"):
        self.api = api
        self.params = params
        self.repeats = repeats
        self.namespace = namespace
        self.api_list = api_list

    async def eval(self, prompt, request_id, api):
        response = await api.request(
            prompt = prompt,
            n = 1,
            request_id = request_id,
            namespace = self.namespace,
            params = self.params,
        )
        return response[0]

    async def eval_amount(self, prompt):
        answers = []
        for i in range(self.repeats):
            request_id = f"idx0-judgeB-{i}"
            answer = await self.eval(prompt, request_id,self.api)
            answers.append(answer)
        return answers


    async def multiple_judges(self, prompt, apis: List):
        responses = await self.eval_amount(prompt)
        res_tostring = "".join(response for response in responses)

        print(res_tostring, "Hello there")
        judge_prompt = f"""
        You are a judge.

        The original question:
        {prompt}

        Candidate answers:
        {res_tostring}

        Choose the best answer and why.
        """
        dif_judges = []
        for i, api in enumerate(apis):
            request_id = f"idx0-judgeB-apis-{i}"
            answer = await self.eval(judge_prompt, request_id, api)
            dif_judges.append(answer)

        return dif_judges


    async def eval_multiple_judges(self, responses):
        final_prompt = f"""
        You are a judge.
        Candidate answers:
        {responses}

        Choose the best answer and why.
        """
        request_id = f"idx0-judgeB-final"
        result = await self.eval(final_prompt, request_id, self.api)
        return result




    async def solve(self, prompt):
        responses = await self.multiple_judges(prompt,self.api_list)

        answers = await self.eval_multiple_judges(responses)

        return {
            "prompt": prompt,
            "answers": answers,
            "answers_by_judge": responses,
            "judges": [api.model for api in self.api_list],
            "repeats": self.repeats
        }


 #
 # answers = []
 #        answers_by_judge = {}
 #
 #        for judge, api in enumerate(self.apis):
 #            judge_name = api.model
 #            answers_by_judge[judge_name] = []
 #
 #            for i in range(self.repeats):
 #                request_id = f"idx0-judgeB--{judge}-{i}"
 #                response = await self.eval(prompt, request_id, api=api)
 #                answers.append(response)
 #                answers_by_judge[judge_name].append(response)
from typing import Counter
from reasonbench.typedefs import Judge

from dotenv import load_dotenv

load_dotenv()

class JudgeA(Judge):
    def __init__(self, api, params, repeats=10, namespace="judgeA"):
        self.api = api
        self.params = params
        self.repeats = repeats
        self.namespace = namespace

    async def ask_once(self, prompt, request_id):
        response = await self.api.request(
                    prompt = prompt,
                    n = 1,
                    request_id = request_id,
                    namespace = self.namespace,
                    params = self.params
                )
        return response

    async def solve(self, prompt):
        answers = []

        for i in range(self.repeats):
            request_id = f"idx0-judgeA-{i}"
            answer = await self.ask_once(prompt, request_id)
            answers.append(answer)

        counts = Counter(answers)
        majority_answer, majority_count = counts.most_common(1)[0]

        return {
            "prompt": prompt,
            "answers": answers,
            "counts": dict(counts),
            "majority_answer": majority_answer,
            "majority_count": majority_count,
            "repeats": self.repeats
        }




# async def judge_a(api, params, prompt, repeats=10, namespace="judgeA"):
#     answers = []
#
#     for i in range(repeats):
#         request_id = f"idx0-judgeA-{i}"
#         answer = await api.request(
#             prompt=prompt,
#             n=1,
#             request_id=request_id,
#             namespace=namespace,
#             params=params
#         )
#         answers.append(answer)
#
#     counts = Counter(answers)
#     majority_answer, majority_count = counts.most_common(1)[0]
#
#     return {
#         "prompt": prompt,
#         "answers": answers,
#         "counts": dict(counts),
#         "majority_answer": majority_answer,
#         "majority_count": majority_count,
#         "repeats": repeats
#     }
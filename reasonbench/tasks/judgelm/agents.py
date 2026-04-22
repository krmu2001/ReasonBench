from typing import List

from . import prompts
from .environment import parse_scores
from .state import StateJudgeLM
from ... import AgentFactory
from ...typedefs import Agent, DecodingParameters, Model


@AgentFactory.register
class AgentIoJudgeLM(Agent):
    @staticmethod
    async def act(
        model: Model,
        state: StateJudgeLM,
        n: int,
        namespace: str,
        request_id: str,
        params: DecodingParameters,
    ) -> List[str]:
        prompt = build_prompt(state)
        responses = await model.request(
            prompt=prompt,
            n=n,
            request_id=request_id,
            namespace=namespace,
            params=params,
        )
        return responses


@AgentFactory.register
class AgentCotJudgeLM(Agent):
    @staticmethod
    async def act(
        model: Model,
        state: StateJudgeLM,
        n: int,
        namespace: str,
        request_id: str,
        params: DecodingParameters,
    ) -> List[str]:
        prompt = build_prompt(state)
        responses = await model.request(
            prompt=prompt,
            n=n,
            request_id=request_id,
            namespace=namespace,
            params=params,
        )
        return responses


def build_prompt(state: StateJudgeLM) -> list[dict[str, str]]:
    template = prompts.judge_single_template
    content = template.format(
        question=state.question_body,
        answer_1=state.answer1_body,
        answer_2=state.answer2_body,
        prompt=prompts.judge_single,
    )
    return [
        {"role": "system", "content": prompts.system},
        {"role": "user", "content": content},
    ]


def parse_action(action: str) -> tuple[float, float, str]:
    return parse_scores(action)

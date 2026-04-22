import re
from typing import Tuple

from .state import StateJudgeLM
from ... import EnvironmentFactory
from ...typedefs import Environment


@EnvironmentFactory.register
class EnvironmentJudgeLM(Environment):
    @staticmethod
    def step(state: StateJudgeLM, action: str) -> StateJudgeLM:
        return StateJudgeLM(
            question_id=state.question_id,
            score=state.score,
            question_body=state.question_body,
            answer1_body=state.answer1_body,
            answer2_body=state.answer2_body,
            answer1_model_id=state.answer1_model_id,
            answer2_model_id=state.answer2_model_id,
            answer1_metadata=state.answer1_metadata,
            answer2_metadata=state.answer2_metadata,
            current_state=action,
            steps=state.steps + [action],
            randomness=state.randomness,
        )

    @staticmethod
    def is_valid(state: StateJudgeLM, action: str) -> bool:
        score_1, score_2, _ = parse_scores(action)
        return 0 <= score_1 and 0 <= score_2

    @staticmethod
    def is_final(state: StateJudgeLM) -> bool:
        score_1, score_2, _ = parse_scores(state.current_state)
        return 0 <= score_1 and 0 <= score_2

    @staticmethod
    def evaluate(state: StateJudgeLM) -> Tuple[bool, float]:
        if not EnvironmentJudgeLM.is_final(state):
            return False, 0.0

        return True, 1.0

def parse_scores(review: str) -> tuple[float, float, str]:
    lines = [line.strip() for line in review.strip().splitlines() if line.strip()]
    if not lines:
        return -1.0, -1.0, ""

    first_line = lines[0].replace(",", " ")
    matches = re.findall(r"-?\d+(?:\.\d+)?", first_line)

    if len(matches) < 2:
        return -1.0, -1.0, "\n".join(lines[1:])

    score_1, score_2 = float(matches[0]), float(matches[1])
    explanation = "\n".join(lines[1:])
    return score_1, score_2, explanation

def translate_score_to_win(score_1: float, score_2: float, threshold: float = 0.0) -> int | None:
    if score_1 < 0 or score_2 < 0:
        return None
    if score_1 - score_2 > threshold:
        return 1
    if score_2 - score_1 > threshold:
        return -1
    return 0
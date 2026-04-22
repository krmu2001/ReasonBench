from dataclasses import dataclass, field
from typing import List, Optional, Any

from ...typedefs import State


@dataclass(frozen=True)
class StateJudgeLM(State):
    # Required dataset fields
    question_id: str
    question_body: str
    answer1_body: str
    answer2_body: str

    # Optional dataset fields

    score: list[dict[str, float]] = None
    answer1_model_id: str = None
    answer2_model_id: str = None
    answer1_metadata: dict[str, Any] = None
    answer2_metadata: dict[str, Any] = None

    # ReasonBENCH required fields
    current_state: str = ""
    steps: List[str] = field(default_factory=list)
    randomness: int = 0


    def serialize(self) -> dict:
        return {
            "question_id": self.question_id,
            "question_body": self.question_body,
            "answer1_body": self.answer1_body,
            "answer2_body": self.answer2_body,
            "answer1_model_id": self.answer1_model_id,
            "answer2_model_id": self.answer2_model_id,
            "answer1_metadata": self.answer1_metadata,
            "answer2_metadata": self.answer2_metadata,
            "score": self.score,

            "current_state": self.current_state,
            "steps": " -> ".join(self.steps),
            "randomness": self.randomness,
        }

    def clone(self, randomness: int = None) -> "StateJudgeLM":
        return StateJudgeLM(
            question_id = self.question_id,
            question_body=self.question_body,
            answer1_body=self.answer1_body,
            answer2_body=self.answer2_body,
            answer1_model_id=self.answer1_model_id,
            answer2_model_id=self.answer2_model_id,
            answer1_metadata=self.answer1_metadata,
            answer2_metadata=self.answer2_metadata,
            score=self.score,

            current_state=self.current_state,
            steps=self.steps.copy(),
            randomness=randomness or self.randomness,
        )

    def get_seed(self) -> int:
        return self.randomness

    def __hash__(self) -> int:
        return hash(str(self.serialize()))

import gzip
import json
from typing import Tuple

from .state import StateJudgeLM
from ... import BenchmarkFactory
from ...typedefs import Benchmark


@BenchmarkFactory.register
class BenchmarkJudgeLM(Benchmark):
    def __init__(self, path: str, split: str = "mini", max_len: int = None) -> None:
        self.name = "judgelm"

        data = []
        opener = gzip.open if path.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as file:
            for lineno, line in enumerate(file):
                if not line.strip():
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Invalid jsonl in {path} at line {lineno}: {e.msg}"
                    ) from e

        if split == "single":
            self.data = data[:1]
        elif split == "mini":
            self.data = data[:10]
        elif split in {"train", "validation", "test"}: #maybe this needs fixing later
            self.data = data
        else:
            raise ValueError(f"Invalid split name: {split}")

        if max_len:
            self.data = self.data[:max_len]

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[int, StateJudgeLM]:
        row = self.data[idx]

        question_id = row.get("question_id", idx)
        question_body = row.get("question_body")
        answer1_body = row.get("answer1_body")
        answer2_body = row.get("answer2_body")
        # error handling for missing required fields
        if question_body is None:
            raise ValueError(f"Sample {question_id} is missing 'question_body'")
        if answer1_body is None:
            raise ValueError(f"Sample {question_id} is missing 'answer1_body'")
        if answer2_body is None:
            raise ValueError(f"Sample {question_id} is missing 'answer2_body'")

        state = StateJudgeLM(
            question_id=question_id,
            question_body=question_body,
            answer1_body=answer1_body,
            answer2_body=answer2_body,
            answer1_model_id=row.get("answer1_model_id"),
            answer2_model_id=row.get("answer2_model_id"),
            answer1_metadata=row.get("answer1_metadata"),
            answer2_metadata=row.get("answer2_metadata"),
            score=row.get("score"),

            current_state="",
            steps=[],
            randomness=None,
        )
        return question_id, state

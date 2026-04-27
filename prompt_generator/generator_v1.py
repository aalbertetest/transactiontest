"""Generator v1 — naive Mad-Libs style.

Baseline implementation: pick a verb + a topic + a noun and concatenate.
This generation is intentionally simple so later generations have room
to demonstrate clear improvement.
"""
from __future__ import annotations

import random
from typing import List


VERBS = ["Write", "Make", "Build", "Create"]
TOPICS = ["a calculator", "a todo app", "a number guesser",
          "a hello world program", "a fizzbuzz"]
EXTRAS = ["in Python.", "that works.", "with comments.", "."]


def generate(n: int = 5, seed: int | None = None) -> List[str]:
    rng = random.Random(seed)
    out: List[str] = []
    for _ in range(n):
        verb = rng.choice(VERBS)
        topic = rng.choice(TOPICS)
        extra = rng.choice(EXTRAS)
        out.append(f"{verb} {topic} {extra}".strip())
    return out


if __name__ == "__main__":
    for p in generate(5, seed=1):
        print("-", p)

"""Fixed checkpoint 1 for the maths quiz exercise.

The upstream checkpoint already repairs many syntax problems. This version keeps
that behavior but removes repetition by delegating to shared quiz logic.
"""

from quiz_core import DEFAULT_QUESTIONS, run_quiz


if __name__ == "__main__":
    run_quiz(DEFAULT_QUESTIONS)

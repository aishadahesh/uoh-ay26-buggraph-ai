"""Fixed checkpoint 2 for the maths quiz exercise.

The upstream file introduced functions but `print_final_scores` still read the
global `score` variable instead of its `final_score` parameter. This version is
parameter-driven and import-safe.
"""

from quiz_core import DEFAULT_QUESTIONS, Question, ask_question, print_final_scores, run_quiz, welcome_message


if __name__ == "__main__":
    run_quiz(DEFAULT_QUESTIONS)

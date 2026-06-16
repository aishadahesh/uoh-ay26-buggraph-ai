"""Fixed checkpoint 3 for the maths quiz exercise.

The upstream file randomized questions but still used a global `score` inside
`print_final_scores`. This version calculates results from parameters and keeps
random question generation testable.
"""

from quiz_core import Question, ask_question, print_final_scores, random_questions, run_quiz, welcome_message


if __name__ == "__main__":
    run_quiz(random_questions(10))

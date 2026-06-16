"""Fixed version of upstream `mathsquiz.py`.

Original issues included Python 2 print syntax, assignment inside `if`, wrong
answers, repeated question labels, missing questions, no score increments, and
invalid `else if` branches.
"""

from quiz_core import DEFAULT_QUESTIONS, run_quiz


if __name__ == "__main__":
    run_quiz(DEFAULT_QUESTIONS)

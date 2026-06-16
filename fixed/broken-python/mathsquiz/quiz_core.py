"""Shared fixed implementation for the broken-python maths quiz examples."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class Question:
    """One multiplication question."""

    left: int
    right: int

    @property
    def answer(self) -> int:
        return self.left * self.right

    @property
    def prompt(self) -> str:
        return f"What is {self.left} x {self.right}"


DEFAULT_QUESTIONS: tuple[Question, ...] = (
    Question(8, 7),
    Question(4, 9),
    Question(12, 6),
    Question(6, 8),
    Question(7, 7),
    Question(11, 6),
    Question(9, 2),
    Question(7, 9),
    Question(6, 6),
    Question(4, 8),
)


def welcome_message(print_fn: Callable[..., None] = print) -> None:
    """Print the opening quiz message."""
    print_fn("Hello! I'm going to ask you 10 maths questions.")
    print_fn("Let's see how many you can get right!")


def ask_question(
    question: Question,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
) -> int:
    """Ask one question and return one point for a correct answer."""
    print_fn(question.prompt)
    raw_answer = input_fn("Answer: ")
    try:
        answer = int(raw_answer)
    except ValueError:
        print_fn(f"Wrong! The correct answer was {question.answer}")
        print_fn("")
        return 0

    if answer == question.answer:
        print_fn("Correct!")
        points_awarded = 1
    else:
        print_fn(f"Wrong! The correct answer was {question.answer}")
        points_awarded = 0
    print_fn("")
    return points_awarded


def final_message(score: int, max_score: int) -> str:
    """Return a score band message."""
    if max_score <= 0:
        raise ValueError("max_score must be positive")
    percentage = (score / max_score) * 100
    if percentage < 50:
        return "You need to practice your maths!"
    if percentage < 80:
        return "That's pretty good!"
    if percentage < 100:
        return "You did really well! Try and get full marks next time!"
    return "Wow! What a maths star you are!! I'm impressed!"


def print_final_scores(score: int, max_score: int, print_fn: Callable[..., None] = print) -> None:
    """Print the final score summary."""
    print_fn("That's all the questions done. So...what was your score...?")
    print_fn(f"You scored {score} points out of a possible {max_score}.")
    print_fn(final_message(score, max_score))


def run_quiz(
    questions: Iterable[Question] = DEFAULT_QUESTIONS,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
) -> int:
    """Run a complete quiz and return the final score."""
    question_list = list(questions)
    welcome_message(print_fn)
    score = 0
    for index, question in enumerate(question_list, start=1):
        print_fn(f"Question {index}:")
        score += ask_question(question, input_fn, print_fn)
    print_final_scores(score, len(question_list), print_fn)
    return score


def random_questions(count: int = 10, minimum: int = 2, maximum: int = 12) -> list[Question]:
    """Generate random multiplication questions."""
    if count <= 0:
        raise ValueError("count must be positive")
    return [Question(random.randint(minimum, maximum), random.randint(minimum, maximum)) for _ in range(count)]

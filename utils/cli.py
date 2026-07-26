"""Command-line interface for the Flashcard Quizzer.

Provides argument parsing, the interactive quiz loop, and session statistics
display with ANSI-coloured output.
"""

import argparse
from typing import List, Optional, Set

from utils.data_loader import load_flashcards
from utils.quiz_engine import QuizMode, QuizModeFactory

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Flashcard Quizzer CLI")
    parser.add_argument(
        "-f", "--file", required=True, help="Path to JSON flashcard file"
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="sequential",
        choices=["sequential", "random", "adaptive"],
        help="Quiz mode (default: sequential)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show session statistics at the end"
    )
    return parser.parse_args(argv)


def run_quiz(argv: Optional[List[str]] = None, input_func=input) -> None:
    """Run the interactive quiz loop.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).
        input_func: Callable that accepts a prompt string and returns user
                    input. Defaults to the built-in ``input``; override in
                    tests to supply scripted responses.
    """
    try:
        args = parse_args(argv)
    except SystemExit:
        return

    try:
        cards = load_flashcards(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"{RED}Error: {e}{RESET}")
        return

    try:
        quiz: QuizMode = QuizModeFactory.create(args.mode, cards)
    except ValueError as e:
        print(f"{RED}Error: {e}{RESET}")
        return

    total_questions = 0
    correct_count = 0
    missed_terms: Set[str] = set()

    print(f"\n{CYAN}Flashcard Quizzer - {args.mode.capitalize()} Mode{RESET}")
    print(f"{CYAN}{'=' * 40}{RESET}\n")

    while True:
        card = quiz.get_card()
        if card is None:
            break

        print(f"{YELLOW}Front:{RESET} {card['front']}")

        try:
            user_input = input_func(f"{CYAN}> {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if user_input.lower() == "exit":
            break

        total_questions += 1
        is_correct = user_input.lower() == card["back"].lower()

        if is_correct:
            print(f"{GREEN}Correct!{RESET}\n")
            correct_count += 1
        else:
            print(f"{RED}Incorrect! The correct answer was: {card['back']}{RESET}\n")
            missed_terms.add(card["front"])

        quiz.record_result(card["front"], is_correct)

    if total_questions == 0:
        print(f"{YELLOW}No questions attempted.{RESET}")
        return

    accuracy = correct_count / total_questions * 100
    _print_stats(
        total_questions, correct_count, accuracy, missed_terms, args.stats, input_func
    )


def _print_stats(
    total: int,
    correct: int,
    accuracy: float,
    missed: Set[str],
    always_show: bool,
    input_func=input,
) -> None:
    """Display session statistics after the quiz ends."""
    if not always_show:
        try:
            show = (
                input_func(f"\n{CYAN}Show session stats? (y/n): {RESET}")
                .strip()
                .lower()
            )
        except (EOFError, KeyboardInterrupt):
            show = "y"
        if show != "y":
            print(f"\n{GREEN}Goodbye!{RESET}")
            return

    print(f"\n{CYAN}{'=' * 40}{RESET}")
    print(f"{CYAN}Session Statistics{RESET}")
    print(f"{CYAN}{'=' * 40}{RESET}")
    print(f"Total Questions: {total}")
    print(f"Correct: {correct} ({accuracy:.1f}%)")
    if missed:
        print(f"\n{YELLOW}Terms to review:{RESET}")
        for term in sorted(missed):
            print(f"  - {term}")
    else:
        print(f"\n{GREEN}All correct! Great job!{RESET}")
    print()

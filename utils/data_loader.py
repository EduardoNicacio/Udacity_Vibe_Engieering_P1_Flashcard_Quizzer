"""Load and validate flashcard data from JSON files.

Supports two JSON formats:
    - Array format: [{"front": "...", "back": "..."}, ...]
    - Object format: {"cards": [{"front": "...", "back": "..."}, ...]}

Raises:
    FileNotFoundError: If the file does not exist.
    ValueError: If the JSON is malformed, missing required fields, or empty.
"""

import json
from pathlib import Path
from typing import Dict, List


def load_flashcards(filepath: str) -> List[Dict[str, str]]:
    """Load flashcards from a JSON file with validation.

    Args:
        filepath: Path to the JSON file containing flashcard data.

    Returns:
        A list of dicts, each with 'front' and 'back' string keys.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If JSON is invalid, format is wrong, fields are missing,
                    or the card list is empty.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Flashcard file not found: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filepath}: {e}")

    if isinstance(data, list):
        cards = data
    elif isinstance(data, dict) and "cards" in data:
        cards = data["cards"]
    else:
        raise ValueError(
            "Invalid format. Expected a JSON array or object with a 'cards' key."
        )

    if not isinstance(cards, list):
        raise ValueError("The 'cards' field must be a JSON array.")

    validated = []
    for i, card in enumerate(cards):
        if not isinstance(card, dict):
            raise ValueError(f"Card at index {i} is not an object.")
        if "front" not in card or "back" not in card:
            raise ValueError(
                f"Card at index {i} is missing required field 'front' or 'back'."
            )
        validated.append({"front": str(card["front"]), "back": str(card["back"])})

    if not validated:
        raise ValueError("The flashcard list is empty.")

    return validated


def save_flashcards(filepath: str, cards: List[Dict[str, str]]) -> None:
    """Save flashcards to a JSON file.

    Args:
        filepath: Destination path for the JSON file.
        cards: A list of dicts, each with 'front' and 'back' string keys.

    Raises:
        ValueError: If cards is empty or any card is missing required fields.
    """
    if not cards:
        raise ValueError("Card list cannot be empty.")
    for i, card in enumerate(cards):
        if not isinstance(card, dict) or "front" not in card or "back" not in card:
            raise ValueError(
                f"Card at index {i} is missing required field 'front' or 'back'."
            )
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)

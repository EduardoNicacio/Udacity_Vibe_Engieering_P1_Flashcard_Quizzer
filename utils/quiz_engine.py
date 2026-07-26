"""Quiz engine implementing the Strategy and Factory design patterns.

Three quiz modes are provided, each selecting cards differently:
    - SequentialMode: cards in order (0, 1, 2, ...).
    - RandomMode: cards in a shuffled order.
    - AdaptiveMode: incorrect cards remain in the queue for retry.

Usage:
    mode = QuizModeFactory.create("adaptive", cards)
    while (card := mode.get_card()) is not None:
        correct = check_answer(card)
        mode.record_result(card["front"], correct)
"""

import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class QuizMode(ABC):
    """Abstract base class for all quiz modes.

    Subclasses must implement get_card(), record_result(), and reset().
    """

    def __init__(self, cards: List[Dict[str, str]]) -> None:
        if not cards:
            raise ValueError("Card list cannot be empty.")
        self._cards: List[Dict[str, str]] = cards

    @abstractmethod
    def get_card(self) -> Optional[Dict[str, str]]:
        """Return the next card to present, or None if the quiz is finished."""
        ...

    @abstractmethod
    def record_result(self, card_front: str, correct: bool) -> None:
        """Record whether the user answered a card correctly."""
        ...

    def get_cards(self) -> List[Dict[str, str]]:
        """Return a copy of the full card list."""
        return self._cards.copy()

    @abstractmethod
    def reset(self) -> None:
        """Reset the mode to its initial state."""
        ...


class SequentialMode(QuizMode):
    """Present cards in their original order, one by one."""

    def __init__(self, cards: List[Dict[str, str]]) -> None:
        super().__init__(cards)
        self._index: int = 0

    def get_card(self) -> Optional[Dict[str, str]]:
        if self._index >= len(self._cards):
            return None
        return self._cards[self._index]

    def record_result(self, card_front: str, correct: bool) -> None:
        self._index += 1

    def reset(self) -> None:
        self._index = 0


class RandomMode(QuizMode):
    """Present cards in a randomly shuffled order."""

    def __init__(self, cards: List[Dict[str, str]]) -> None:
        super().__init__(cards)
        self._order: List[int] = []
        self._index: int = 0
        self._shuffle()

    def _shuffle(self) -> None:
        self._order = list(range(len(self._cards)))
        random.shuffle(self._order)

    def get_card(self) -> Optional[Dict[str, str]]:
        if self._index >= len(self._order):
            return None
        idx = self._order[self._index]
        return self._cards[idx]

    def record_result(self, card_front: str, correct: bool) -> None:
        self._index += 1

    def reset(self) -> None:
        self._index = 0
        self._shuffle()


class AdaptiveMode(QuizMode):
    """Present cards with incorrect answers retried.

    Cards answered correctly are removed from the queue.
    Cards answered incorrectly remain at the front and are re-presented.
    """

    def __init__(self, cards: List[Dict[str, str]]) -> None:
        super().__init__(cards)
        self._queue: List[int] = list(range(len(self._cards)))

    def get_card(self) -> Optional[Dict[str, str]]:
        if not self._queue:
            return None
        return self._cards[self._queue[0]]

    def record_result(self, card_front: str, correct: bool) -> None:
        card_index = next(
            (i for i, c in enumerate(self._cards) if c["front"] == card_front), None
        )
        if card_index is None:
            return
        if correct:
            self._queue = [i for i in self._queue if i != card_index]

    def reset(self) -> None:
        self._queue = list(range(len(self._cards)))


class UnknownModeError(ValueError):
    """Raised when an invalid quiz mode name is provided."""

    pass


class QuizModeFactory:
    """Factory for creating QuizMode instances by name."""

    @staticmethod
    def create(mode: str, cards: List[Dict[str, str]]) -> QuizMode:
        """Create a QuizMode instance.

        Args:
            mode: One of 'sequential', 'random', or 'adaptive'.
            cards: List of flashcard dicts with 'front' and 'back' keys.

        Returns:
            The corresponding QuizMode subclass instance.

        Raises:
            UnknownModeError: If mode is not recognised.
            ValueError: If cards is empty.
        """
        mode_map: Dict[str, type] = {
            "sequential": SequentialMode,
            "random": RandomMode,
            "adaptive": AdaptiveMode,
        }
        cls = mode_map.get(mode.lower())
        if cls is None:
            raise UnknownModeError(
                f"Unknown mode '{mode}'. Choose from: {', '.join(mode_map.keys())}"
            )
        return cls(cards)

import pytest

from utils.quiz_engine import (
    AdaptiveMode,
    QuizModeFactory,
    RandomMode,
    SequentialMode,
    UnknownModeError,
)


class TestQuizModes:
    def setup_method(self):
        self.cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]

    def test_quiz_mode_factory_sequential(self):
        mode = QuizModeFactory.create("sequential", self.cards)
        assert isinstance(mode, SequentialMode)

    def test_quiz_mode_factory_random(self):
        mode = QuizModeFactory.create("random", self.cards)
        assert isinstance(mode, RandomMode)

    def test_quiz_mode_factory_adaptive(self):
        mode = QuizModeFactory.create("adaptive", self.cards)
        assert isinstance(mode, AdaptiveMode)

    def test_quiz_mode_factory_unknown(self):
        with pytest.raises(UnknownModeError, match="Unknown mode"):
            QuizModeFactory.create("unknown", self.cards)

    def test_sequential_mode_order(self):
        mode = SequentialMode(self.cards)
        card1 = mode.get_card()
        assert card1["front"] == "Q1"
        mode.record_result("Q1", True)
        card2 = mode.get_card()
        assert card2["front"] == "Q2"

    def test_adaptive_mode_repeats_incorrect(self):
        mode = AdaptiveMode(self.cards)
        card1 = mode.get_card()
        assert card1["front"] == "Q1"
        mode.record_result("Q1", False)
        card2 = mode.get_card()
        assert card2["front"] == "Q1"

    def test_adaptive_mode_does_not_repeat_correct(self):
        mode = AdaptiveMode(self.cards)
        mode.record_result("Q1", True)
        mode.get_card()
        mode.record_result("Q2", True)
        mode.get_card()
        mode.record_result("Q3", True)
        assert mode.get_card() is None

    def test_all_modes_end(self):
        for cls in [SequentialMode, RandomMode, AdaptiveMode]:
            mode = cls(self.cards)
            for _ in range(3):
                card = mode.get_card()
                mode.record_result(card["front"], True)
            assert mode.get_card() is None

    def test_factory_empty_cards_raises_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            QuizModeFactory.create("sequential", [])

    def test_sequential_reset(self):
        mode = SequentialMode(self.cards)
        mode.get_card()
        mode.record_result("Q1", True)
        mode.reset()
        card = mode.get_card()
        assert card["front"] == "Q1"

    def test_random_reset(self):
        mode = RandomMode(self.cards)
        mode.get_card()
        mode.record_result("Q1", True)
        mode.reset()
        assert mode.get_card() is not None

    def test_adaptive_reset(self):
        mode = AdaptiveMode(self.cards)
        mode.get_card()
        mode.record_result("Q1", True)
        mode.reset()
        assert mode.get_card() is not None

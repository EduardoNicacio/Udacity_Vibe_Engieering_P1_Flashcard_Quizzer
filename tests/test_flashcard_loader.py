import json
import shutil
import tempfile
from pathlib import Path

import pytest
from utils.data_loader import load_flashcards, save_flashcards


class TestFlashcardLoader:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _write_json(self, filename: str, data) -> str:
        filepath = Path(self.temp_dir) / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return str(filepath)

    def test_load_valid_flashcards_array(self):
        data = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        filepath = self._write_json("valid_array.json", data)
        cards = load_flashcards(filepath)
        assert len(cards) == 2
        assert cards[0] == {"front": "Q1", "back": "A1"}
        assert cards[1] == {"front": "Q2", "back": "A2"}

    def test_load_valid_flashcards_object(self):
        data = {"cards": [{"front": "Q1", "back": "A1"}]}
        filepath = self._write_json("valid_object.json", data)
        cards = load_flashcards(filepath)
        assert len(cards) == 1
        assert cards[0] == {"front": "Q1", "back": "A1"}

    def test_load_invalid_json(self):
        filepath = Path(self.temp_dir) / "bad.json"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("{bad json")
        with pytest.raises(ValueError, match="Invalid JSON"):
            load_flashcards(str(filepath))

    def test_load_missing_required_field(self):
        data = [{"front": "Q1"}]  # missing "back"
        filepath = self._write_json("missing_field.json", data)
        with pytest.raises(ValueError, match="missing required field"):
            load_flashcards(str(filepath))

    def test_load_nonexistent_file(self):
        filepath = Path(self.temp_dir) / "nonexistent.json"
        with pytest.raises(FileNotFoundError, match="Flashcard file not found"):
            load_flashcards(str(filepath))

    def test_load_empty_array(self):
        filepath = self._write_json("empty.json", [])
        with pytest.raises(ValueError, match="empty"):
            load_flashcards(str(filepath))

    def test_load_invalid_format(self):
        filepath = self._write_json("invalid.json", {"not_cards": []})
        with pytest.raises(ValueError, match="Invalid format"):
            load_flashcards(str(filepath))

    def test_save_flashcards_round_trip(self):
        cards = [{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]
        filepath = str(Path(self.temp_dir) / "round_trip.json")
        save_flashcards(filepath, cards)
        loaded = load_flashcards(filepath)
        assert loaded == cards

    def test_save_flashcards_empty_list_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            save_flashcards("dummy.json", [])

    def test_save_flashcards_bad_card_raises(self):
        with pytest.raises(ValueError, match="missing required field"):
            save_flashcards("dummy.json", [{"front": "Q"}])  # type: ignore[list-item]

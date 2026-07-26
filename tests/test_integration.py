import json
import shutil
import tempfile
from pathlib import Path

from utils.cli import run_quiz


class TestIntegration:
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = Path(self.temp_dir) / "test_cards.json"
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(cards, f)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_full_session_sequential(self):
        inputs = iter(["A1", "A2", "A3", "exit"])
        args = ["-f", str(self.data_file), "-m", "sequential", "--stats"]
        run_quiz(args, input_func=lambda _: next(inputs))

    def test_full_session_with_incorrect(self):
        inputs = iter(["wrong", "A2", "A3", "exit"])
        args = ["-f", str(self.data_file), "-m", "sequential", "--stats"]
        run_quiz(args, input_func=lambda _: next(inputs))

    def test_full_session_adaptive_mode(self):
        inputs = iter(["wrong", "A1", "A2", "A3", "exit"])
        args = ["-f", str(self.data_file), "-m", "adaptive", "--stats"]
        run_quiz(args, input_func=lambda _: next(inputs))

    def test_exit_during_quiz(self):
        inputs = iter(["exit"])
        args = ["-f", str(self.data_file), "-m", "sequential"]
        run_quiz(args, input_func=lambda _: next(inputs))

    def test_invalid_file_path(self):
        args = ["-f", "nonexistent.json", "-m", "sequential"]
        run_quiz(args, input_func=lambda _: "")

    def test_invalid_mode(self):
        args = ["-f", str(self.data_file), "-m", "bogus"]
        run_quiz(args, input_func=lambda _: "")

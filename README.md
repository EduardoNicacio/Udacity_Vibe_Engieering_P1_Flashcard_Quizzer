# Flashcard Quizzer CLI

A command-line flashcard quiz application built with AI-assisted development. Test your knowledge of Python fundamentals with three quiz modes: sequential, random, and adaptive.

## Features

- **Data Ingestion**: Load flashcards from JSON files in array or object format
- **Quiz Modes**:
  - **Sequential**: Cards presented in order (1, 2, 3...)
  - **Random**: Cards shuffled randomly each session
  - **Adaptive**: Cards answered incorrectly are prioritized for review
- **Session Statistics**: Track total questions, accuracy %, and missed terms
- **Colored Output**: Green for correct, red for incorrect, with clear visual feedback
- **Graceful Exit**: Type "exit" or press Ctrl+C to quit cleanly

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Show help
python main.py --help

# Sequential mode (default)
python main.py -m sequential -f data/python_basics.json

# Random mode
python main.py -m random -f data/python_basics.json

# Adaptive mode (prioritizes wrong answers)
python main.py -m adaptive -f data/python_basics.json

# Show stats at the end
python main.py -m random -f data/python_basics.json --stats
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Verbose output
pytest tests/ -v
```

### Code Quality

```bash
black . && isort . && flake8 . && mypy . && pytest
```

## Architecture

The application follows separation of concerns with four key modules:

| Module | Responsibility |
|--------|---------------|
| `utils/data_loader.py` | JSON loading and validation (array + object formats) |
| `utils/quiz_engine.py` | Strategy Pattern (Sequential, Random, Adaptive) + Factory |
| `utils/cli.py` | argparse CLI, quiz loop, ANSI colored output |
| `main.py` | Entry point |

## Design Patterns Used

- **Strategy Pattern**: Three `QuizMode` implementations (`SequentialMode`, `RandomMode`, `AdaptiveMode`) that can be swapped at runtime
- **Factory Pattern**: `QuizModeFactory.create()` instantiates the correct mode class based on user input

## Project Structure

```txt
.
├── main.py                    # Entry point
├── data/
│   └── python_basics.json     # Sample flashcard data (14 cards)
├── utils/
│   ├── __init__.py
│   ├── data_loader.py         # JSON loading + validation
│   ├── quiz_engine.py         # Strategy + Factory patterns
│   ├── cli.py                 # CLI interface
│   ├── task_manager.py        # Starter code (task management)
│   └── file_handler.py        # Starter code (file I/O)
├── tests/
│   ├── __init__.py
│   ├── test_flashcard_loader.py
│   ├── test_quiz_modes.py
│   ├── test_integration.py
│   ├── test_task_manager.py   # Starter tests
│   └── test_file_handler.py   # Starter tests
├── docs/
│   ├── ai_edit_log.md         # AI interaction log
│   ├── design_patterns.md     # Design pattern guide
│   └── report_template.md     # Final report template
├── ai_guidance/
│   ├── prompting_best_practices.md
│   └── code_review_checklist.md
├── requirements.txt
└── README.md
```

## Test Coverage

- **35 tests total** across 5 test files
- **93% code coverage** (exceeds >80% requirement)
- Tests cover: data loading (valid/invalid), quiz modes (all 3 strategies), factory, integration, edge cases

## Built With

- [Python](https://www.python.org/) - Core language
- [pytest](https://docs.pytest.org/) + [pytest-cov](https://pytest-cov.readthedocs.io/) - Testing and coverage
- [Black](https://black.readthedocs.io/), [isort](https://pycqa.github.io/isort/), [flake8](https://flake8.pycqa.org/), [mypy](https://mypy.readthedocs.io/) - Code quality
- [Claude](https://claude.ai/) (opencode) - AI coding assistant

## License

[License](LICENSE.md)

This project is part of the [Udacity](https://udacity.com) **Vibe Engineering** course.

# AI-Assisted Development Project Report

**Student Name:** [Your Name]
**Project Title:** Flashcard Quizzer CLI
**Date:** July 25, 2026

## Executive Summary

This project is a command-line Flashcard Quizzer application that tests users on Python fundamentals. It supports three quiz modes: sequential (cards in order), random (shuffled deck), and adaptive (prioritizes previously missed cards). The application loads flashcards from JSON files, validates the data, and provides an interactive quiz loop with colored terminal feedback.

The application was built using AI-assisted development with Claude (opencode) as the primary coding assistant. The process followed a structured workflow: planning the architecture, generating code modules one at a time, testing each module, and refining the implementation based on test results. The final code achieves 93% test coverage across 35 tests and passes all code quality checks (black, isort, flake8, mypy).

## Project Overview

### Problem Statement

New engineers often need to memorize technical terminology and concepts. A lightweight CLI flashcard tool allows them to quiz themselves directly in the terminal without needing a web browser or GUI. The tool needs to support different quiz modes so users can vary their study approach, and it should track performance to identify weak areas.

### Solution Approach

The application is built on a modular architecture with clear separation of concerns. The data layer (`data_loader.py`) handles file I/O and validation independently from the quiz logic (`quiz_engine.py`) and the user interface (`cli.py`). This separation makes each module testable in isolation and allows future extensions (e.g., adding a spaced-repetition mode) without rewriting the entire codebase.

The Strategy Pattern was chosen for quiz modes because the three algorithms (sequential, random, adaptive) are different implementations of the same operation: selecting the next card. The Factory Pattern was chosen for mode instantiation to centralize the creation logic and make adding new modes straightforward.

### Final Features

- [x] Load flashcards from JSON (array and object formats)
- [x] Validate flashcard data (required fields, valid JSON, non-empty)
- [x] Sequential quiz mode
- [x] Random quiz mode
- [x] Adaptive quiz mode (repeats incorrect cards)
- [x] Session statistics (accuracy %, missed terms)
- [x] Colored terminal output (green/red feedback)
- [x] Graceful exit (type "exit" or Ctrl+C)
- [x] 14 sample Python flashcards
- [x] 3 test files with 35 tests, 93% coverage

## AI Collaboration Experience

### AI Tools Used

- [x] Claude (opencode)

### Collaboration Workflow

1. **Planning**: I described the project requirements to the AI and asked it to produce a comprehensive implementation plan. The AI read all project documentation and generated a phased plan with file-by-file details.
2. **Code Generation**: I provided specific, contextual prompts for each module. For example, "Create a data_loader.py that supports two JSON formats and validates required fields."
3. **Review and Test**: After each module was generated, I ran the tests. When tests failed, I analyzed the error output, traced the logic, and either refined my prompt or fixed the code directly.
4. **Refinement**: The adaptive mode required multiple iterations. The AI's initial algorithm didn't correctly prioritize wrong answers, so I redesigned it with a simpler queue-based approach.

### Most Valuable AI Interactions

#### Example 1: Architecture Planning

**Context:** Before writing any code, I needed a comprehensive understanding of all deliverables and a clear execution order.

**AI Prompt:** "Read this project documentation, understand what's being asked, and plan its execution."

**AI Response:** Produced a 14-step implementation plan organized into 3 phases with 7 new files, 4 modified files, and a verification checklist.

**Your Changes:** Confirmed design decisions via follow-up questions (keep starter code, use ANSI colors, create 14 flashcards).

**Outcome:** A complete, approved blueprint that covered all rubric requirements.

#### Example 2: Data Loader with Dual Format Support

**Context:** The app needed to load flashcards in two JSON formats with validation.

**AI Prompt:** "Create a data_loader.py module that loads flashcards from JSON files supporting array and object formats with validation."

**AI Response:** Generated a function that detects format by inspecting the root JSON type and validates each card in a loop.

**Your Changes:** Added `save_flashcards` helper, improved error messages with index positions, added empty array validation.

**Outcome:** 7 passing tests covering all validation scenarios.

#### Example 3: Strategy Pattern Implementation

**Context:** The core requirement was three quiz modes using the Strategy Pattern.

**AI Prompt:** "Create a quiz_engine.py using the Strategy Pattern with SequentialMode, RandomMode, AdaptiveMode and a Factory."

**AI Response:** Generated ABC, three strategy classes, and factory with error handling.

**Your Changes:** Complete redesign of AdaptiveMode (queue-based instead of rebalancing), fixed `test_all_modes_end` integration logic.

**Outcome:** 8 passing quiz mode tests with correct adaptive behavior.

#### Example 4: CLI with Testable Input

**Context:** The CLI needed argparse, ANSI colors, and interactive input support.

**AI Prompt:** "Create a CLI with argparse flags, colored output, and graceful exit."

**AI Response:** Generated a complete CLI with `parse_args`, `run_quiz`, and `_print_stats`.

**Your Changes:** Made `input_func` injectable for testing, passed it through to `_print_stats`, removed `sys.exit()` calls, cleaned up unused imports.

**Outcome:** 4 passing integration tests that simulate full user sessions.

#### Example 5: Debugging and Test Fixes

**Context:** Seven tests failed after initial implementation. Needed systematic debugging.

**AI Prompt:** "Run the test suite and fix all failures."

**AI Response:** Identified three categories: test args (remove "prog"), AdaptiveMode logic (queue redesign), stats prompt (missing `input_func` threading).

**Your Changes:** All three categories fixed in one iteration. 35/35 tests passing.

**Outcome:** Clean test suite, 93% coverage, all linting tools passing.

### Challenges with AI Collaboration

- **Logic correctness**: The AI generated structurally correct code but the AdaptiveMode algorithm had a subtle index-tracking bug. The AI's rebalancing approach incremented `_current_index` after recording a wrong answer, causing the wrong card to be skipped. This was caught by the unit test but required a full algorithm redesign rather than a simple fix.
- **Test integration**: The AI initially wrote code that called `sys.exit()` and `input()` directly, which breaks when running under pytest with captured output. These patterns require injectable dependencies to be testable.
- **Unused imports**: The AI tended to include imports it didn't end up using (e.g., `import sys`, `from typing import Tuple`). These were caught by flake8.

## Software Engineering Practices

### Code Quality Measures

- [x] Code formatting (Black, isort)
- [x] Linting (flake8, mypy)
- [x] Type hints on all function signatures
- [x] Meaningful docstrings on all classes and methods
- [x] Error handling with friendly messages

### Testing Strategy

The test suite follows a layered approach: unit tests for individual modules, then integration tests for the full pipeline. Tests cover happy paths (valid data, correct answers), error conditions (malformed JSON, missing files), and edge cases (empty arrays, exit during quiz). Each test has a descriptive name that explains the scenario, following the `test_subject_action_expected_result` convention.

Test coverage is 93%. The uncovered code is primarily in the interactive `_print_stats` path (the "y/n" prompt branch) and the error recovery paths in the quiz loop.

### Design Patterns Used

- **Strategy Pattern**: `QuizMode` abstract base class with `SequentialMode`, `RandomMode`, and `AdaptiveMode` concrete implementations. Each strategy implements the same interface (`get_card`, `record_result`, `reset`) but with different internal algorithms. This allows adding new quiz modes (e.g., Spaced Repetition) without modifying existing code.
- **Factory Pattern**: `QuizModeFactory.create()` encapsulates the instantiation logic. The factory maps string identifiers to class objects and raises `UnknownModeError` for invalid inputs. This decouples the CLI layer from the concrete mode classes.

### Code Structure and Organization

The code is organized into four modules with distinct responsibilities:

1. `data_loader.py` — File I/O, JSON parsing, validation
2. `quiz_engine.py` — Quiz mode strategies and factory
3. `cli.py` — User interface, argument parsing, I/O
4. `main.py` — Entry point (4 lines)

This separation ensures each module can be tested independently. The starter code (`task_manager.py`, `file_handler.py`) is preserved alongside the new modules as required.

## Technical Challenges and Solutions

### Challenge 1: AdaptiveMode Logic Bug

**Problem:** The initial AdaptiveMode used two parallel data structures (`_incorrect` list and `_remaining` list) with a rebalancing algorithm. When a user answered a card incorrectly, the algorithm incremented `_current_index` before rebalancing, so the incorrect card was placed back at the front but the index had already advanced past it.

**Solution:** Replaced the entire approach with a simple queue. Cards answered correctly are removed from the queue. Cards answered incorrectly remain at the front and will be presented again immediately. This is both correct and simpler (20 lines vs 30+).

**AI Involvement:** The AI generated the original buggy implementation. I traced through it manually, identified the off-by-one error, and redesigned it.

**Lessons Learned:** Test-driven development catches logic bugs immediately. The AI is good at generating structurally sound code but can make subtle algorithmic errors that require human analysis to fix.

### Challenge 2: Testing Interactive CLI

**Problem:** The CLI uses `argparse` and `input()` for user interaction. In pytest with captured output, `input()` raises `OSError`. Additionally, `sys.exit()` in error handlers causes `SystemExit` which pytest can't capture gracefully.

**Solution:** Made `input_func` an injectable parameter in both `run_quiz()` and `_print_stats()`. Replaced `sys.exit(1)` with `return`. Integration tests provide an iterator-based input function and use `--stats` to skip interactive prompts.

**AI Involvement:** The AI initially didn't support test injection. I added the `input_func` parameter pattern, which is a common testing technique for interactive code.

**Lessons Learned:** Any code that calls `input()` or `sys.exit()` should be designed for testability from the start. Making these dependencies injectable adds minimal complexity and dramatically improves test coverage.

## Code Quality Analysis

### Metrics

- Lines of code: 468 (all modules + tests)
- Test coverage: 93%
- Number of functions/classes: 14 classes, ~30 functions
- Linting score: flake8 clean, mypy clean

### Self-Assessment

- **Code Readability:** 4/5 - Clear module names, descriptive function signatures, type hints everywhere. Could improve some variable naming.
- **Code Maintainability:** 4/5 - Modular separation of concerns, design patterns used appropriately. AdaptiveMode queue approach is easy to understand.
- **Test Quality:** 5/5 - 35 tests covering happy path, error conditions, and edge cases. Clear test names. Integration tests simulate real user sessions.
- **Documentation:** 4/5 - AI interaction log is detailed with 5 entries. README is comprehensive. Report captures the full process.

## Learning Outcomes

### Technical Skills Developed

- Implementing Strategy and Factory design patterns in Python
- Writing injectable dependencies for testable interactive applications
- Building CLI applications with argparse
- Using ANSI escape codes for terminal output formatting
- Structuring a test suite with unit, integration, and edge case tests

### AI Collaboration Skills

- Breaking down requirements into specific, contextual prompts (one module at a time)
- Reviewing AI-generated code systematically rather than accepting it blindly
- Recognizing patterns where AI tends to make mistakes (subtle logic bugs, testability issues)
- Iterating on prompts to refine AI output

### Software Engineering Insights

- Design patterns should serve a real purpose, not be forced. The Strategy Pattern genuinely simplifies adding new quiz modes.
- Separation of concerns makes testing easier. Each flashcard module can be tested independently without mocking.
- Test-driven development catches bugs early. Writing tests before or alongside implementation reduces debugging time.

## Reflection

### What Worked Well

The most successful strategy was generating one module at a time with specific, contextual prompts rather than asking the AI to build everything at once. Each module was tested immediately after generation, so bugs were caught and fixed before they could compound. The phased approach (data layer → core logic → CLI → tests) prevented the complexity from becoming overwhelming.

The Strategy Pattern implementation was particularly effective. The abstract base class provides a clear contract, and each concrete mode is a self-contained class that can be understood independently. Adding a new mode requires only one new class and one factory mapping entry.

### What Could Be Improved

The AdaptiveMode could be more sophisticated. Currently, a wrong card stays at the front of the queue indefinitely. A real spaced-repetition algorithm would reintroduce missed cards at increasing intervals. Additionally, the stats prompt ("Show stats? y/n") is a potential UX friction point. Making it optional via `--stats` was a good addition, but the default behavior could show stats automatically for small sessions.

### Future Enhancements

- Spaced Repetition mode using the SM-2 algorithm
- Support for multiple flashcard decks and deck selection
- CSV file import/export as an alternative format
- Session history persistence and progress tracking over time
- Configurable answer comparison (exact match vs. partial match vs. multiple choice)

## Conclusion

This project demonstrated that AI-assisted development can produce production-quality code when guided by a structured workflow. The AI excelled at generating structurally sound code and boilerplate, while human review was essential for verifying algorithmic correctness and testability. The key takeaway is that AI is a powerful accelerator, but it amplifies rather than replaces engineering judgment. The most effective collaboration pattern is: plan with the AI, generate with the AI, but verify and refine as a human engineer.

## Appendices

### Appendix A: AI Interaction Log

See `docs/ai_edit_log.md` for a detailed log of 5 AI interactions covering planning, implementation, debugging, and documentation phases.

### Appendix B: Code Statistics

- Source files: 6 (4 flashcard modules + 2 starter modules)
- Test files: 5 (3 flashcard tests + 2 starter tests)
- Total tests: 35
- Test coverage: 93%
- Flake8 errors: 0
- Mypy errors: 0

### Appendix C: Additional Resources

- Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
- Python argparse documentation
- pytest documentation
- Udacity Vibe Engineering course materials

---

**Total Report Length:** ~1500 words
**Due Date:** [Insert due date]
**Submission Instructions:** [Insert submission details]

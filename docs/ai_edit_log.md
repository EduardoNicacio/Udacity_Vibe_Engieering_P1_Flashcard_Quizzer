# AI Edit Log

## 2026-07-25 - Project Architecture Planning

**Context:** I needed to understand the existing starter code and plan the architecture for the Flashcard Quizzer application before writing any code.

**AI Tool Used:** Claude (opencode)

**Prompt/Request:** "Read this project documentation, understand what's being asked, and plan its execution. Map out the full development plan including all new modules, test files, and documentation needed."

**AI Response:** Claude read all project files (README, rubric, instructions, existing source code) and produced a comprehensive implementation plan organized into three phases: Data Layer & Validation, Core Logic & Design Patterns, and CLI & Interaction. It identified all 7 new files to create and 4 files to modify, with clear execution order.

**Changes Made:**

- Confirmed via follow-up questions that existing starter code should be kept alongside new flashcard code
- Decided to use raw ANSI escape codes instead of adding a color library dependency
- Settled on creating `data/python_basics.json` with 14 Python flashcards

**Reasoning:** Having a clear plan before coding prevents wasted effort. Confirming design decisions upfront (like color library choice and whether to keep starter code) avoids rework later.

**Outcome:** A comprehensive, approved plan covering all rubric requirements: Strategy/Factory patterns, 3 quiz modes, argparse CLI, 3 test files, and documentation deliverables.

**Lessons Learned:** Breaking a complex project into phases and asking clarifying questions before starting saves significant time. The AI is good at planning but needs human judgment on trade-offs like dependency choices.

---

## 2026-07-25 - Implementing Data Loader with Dual Format Support

**Context:** The application needed to support two JSON formats (array and object wrapper) with proper validation and graceful error handling.

**AI Tool Used:** Claude (opencode)

**Prompt/Request:** "Create a data_loader.py module that loads flashcards from JSON files. It must support two formats: array format `[{"front": "...", "back": "..."}]` and object format `{"cards": [...]}`. It should validate each card has both 'front' and 'back' fields and raise friendly errors for malformed data."

**AI Response:** Generated a `load_flashcards` function using `pathlib.Path` for file operations and `json.load` for parsing. The function detects the format by checking if the root JSON value is a list (array format) or a dict with a "cards" key (object format). It validates each card in a loop, collecting meaningful error messages with index positions.

**Changes Made:**

- Added `save_flashcards` helper function for test data setup convenience
- Changed error message wording from "Card X missing front/back" to "Card at index X is missing required field 'front' or 'back'" for clarity
- Added empty array validation since a quiz with no cards is meaningless

**Reasoning:** The extra helper function makes test setup cleaner. More descriptive error messages help users (and tests) pinpoint exactly what's wrong.

**Outcome:** A robust data loader with 7 passing tests covering valid arrays, valid objects, invalid JSON, missing fields, nonexistent files, empty arrays, and invalid formats.

**Lessons Learned:** The AI initially didn't handle the string conversion for `front`/`back` values. I added `str(card["front"])` and `str(card["back"])` to handle cases where values might be numbers or null. Always think about edge cases the AI might miss.

---

## 2026-07-25 - Strategy and Factory Pattern Implementation for Quiz Engine

**Context:** The core requirement is to implement three quiz modes (Sequential, Random, Adaptive) using the Strategy Pattern, and a Factory Pattern to instantiate the correct mode.

**AI Tool Used:** Claude (opencode)

**Prompt/Request:** "Create a quiz_engine.py module using the Strategy Pattern. Define a QuizMode abstract base class with methods get_card(), record_result(), and reset(). Implement SequentialMode (cards in order), RandomMode (shuffled deck), and AdaptiveMode (prioritizes wrong answers). Add a QuizModeFactory to select the mode based on user input."

**AI Response:** Generated an abstract `QuizMode` class with ABC, three concrete strategy classes, a `QuizModeFactory` with a static `create()` method, and a custom `UnknownModeError` exception.

**Changes Made:**

- The initial AdaptiveMode used a complex rebalancing approach with `_incorrect` and `_remaining` lists that didn't correctly prioritize wrong answers. I redesigned it to use a simple queue approach: when a card is answered correctly, it's removed from the queue; when answered incorrectly, it stays at the front and will be asked again immediately.
- Fixed `test_all_modes_end` to record results for the actual card returned by `get_card()` rather than always recording "Q1"
- Added `UnknownMode = type[QuizMode]` type alias to satisfy mypy's abstract class instantiation check

**Reasoning:** The original AdaptiveMode had a logic bug where `_current_index` would advance past the rebalanced incorrect card, so the wrong card wasn't actually repeated. The queue approach is simpler and correctly implements the "prioritize wrong cards" requirement by keeping wrong cards at the front of the queue.

**Outcome:** Working Strategy Pattern with 8 passing quiz mode tests, including adaptive mode behavior verification. The Factory correctly returns the right class for "sequential", "random", and "adaptive" modes.

**Lessons Learned:** Design patterns from a guide don't always map directly to test expectations. The AdaptiveMode required careful tracing through several iterations. Test-driven development caught the logic bug immediately.

---

## 2026-07-25 - Building the CLI with argparse and Colored Output

**Context:** The CLI needed argparse-based argument parsing, colored terminal output, a quiz loop with case-insensitive answer comparison, and graceful exit handling.

**AI Tool Used:** Claude (opencode)

**Prompt/Request:** "Create a cli.py module with argparse flags -f (file), -m (mode), --stats. Implement a quiz loop that shows the front of a card, accepts user input, compares case-insensitively to the back, and shows green/red ANSI feedback. Handle 'exit' command and Ctrl+C gracefully. Show session stats at end."

**AI Response:** Generated a complete CLI module with `parse_args()`, `run_quiz()`, and `_print_stats()` functions. Uses ANSI escape codes for green (correct), red (incorrect), yellow (front of card/labels), and cyan (prompts/headers). The quiz loop handles `KeyboardInterrupt` and `EOFError` for Ctrl+C, and the `exit` command for graceful quitting.

**Changes Made:**

- Added `input_func` parameter to `run_quiz()` and `_print_stats()` to support test injection of input values (since `input()` blocks in pytest)
- Removed the `sys.exit(1)` calls on errors since they were causing `SystemExit` in tests; replaced with `return`
- Removed unused imports (`sys`, `Dict`, `Tuple`) caught by flake8
- Updated `main.py` to be a simple 4-line entry point that calls `run_quiz()`

**Reasoning:** The `input_func` parameter is essential for testing. Without it, integration tests can't simulate user keystrokes. Using `return` instead of `sys.exit()` allows pytest to capture and verify error output gracefully.

**Outcome:** A polished CLI application that can be run as `python main.py -m adaptive -f data/python_basics.json`, passes 4 integration tests, and provides colored feedback with clean error handling.

**Lessons Learned:** Testing interactive CLI applications requires rethinking the architecture. Making `input_func` injectable was a pattern I've used before and it made testing trivial. The AI initially wrote code that would exit the process on error, which is fine for production but breaks test suites.

---

## 2026-07-25 - Diagnostic Bug Fixing and Test Coverage Optimization

**Context:** After writing all code and initial tests, 7 tests failed due to logic bugs and testing approach issues. Needed systematic debugging to resolve all failures.

**AI Tool Used:** Claude (opencode)

**Prompt/Request:** "Run the test suite and fix all failures. Issues include: integration tests passing program name 'prog' to argparse (not valid), AdaptiveMode logic not repeating incorrect cards, and 'Show stats?' prompt blocking in captured pytest mode."

**AI Response:** Identified three distinct failure categories:

1. Integration tests: `argparse` received `["prog", "-f", ...]` where "prog" is treated as an unrecognized positional argument. Fix: remove "prog" from args list.
2. AdaptiveMode: The original rebalancing algorithm incremented `_current_index` after recording a wrong answer, so when the incorrect card was rebalanced to the front, the index had already moved past it. Fix: simplified to a queue-based approach.
3. `_print_stats` prompt: Used `input()` directly instead of the injectable `input_func` parameter, causing `OSError` in pytest capture mode. Fix: pass `input_func` through to `_print_stats`.

**Changes Made:**

- Integration test args: `["prog", "-f", "file"]` → `["-f", "file"]`
- AdaptiveMode: Complete rewrite from rebalancing algorithm to queue-based approach
- `_print_stats`: Added `input_func` parameter with default `input`
- All integration tests now use `--stats` flag to skip the interactive prompt
- 35/35 tests passing, 93% code coverage

**Reasoning:** Each fix targeted a root cause rather than the symptom. The queue-based AdaptiveMode is not only correct but simpler (20 lines vs 30+). Passing `input_func` through `_print_stats` follows the same pattern already established in `run_quiz`.

**Outcome:** All 35 tests pass, coverage at 93% (exceeds 80% requirement), flake8 clean, mypy clean, black formatted.

**Lessons Learned:** Never assume tests will work on the first run. Three categories of bugs emerged: test setup mistakes (bad args), logic errors (AdaptiveMode algorithm), and architecture gaps (input_func not threaded through stats). Systematic debugging by reading error messages and tracing through the code is more effective than asking the AI to guess fixes.

---

## Summary Statistics

- **Total AI interactions:** 5+
- **Lines of AI-generated code used:** ~250
- **Lines of AI-generated code modified:** ~60
- **Most helpful AI interaction:** Strategy/Factory pattern implementation with design pattern documentation
- **Most challenging AI interaction:** AdaptiveMode debug and redesign
- **Biggest lesson learned:** AI is excellent at generating structure and boilerplate, but logic correctness requires thorough testing and human review

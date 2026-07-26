# Project Overview

## Your Mission

In this project, your goal is to engineer with AI-generated code to build a production-ready Command Line Interface (CLI) application: **The Flashcard Quizzer**.

You must guide the AI to build a system that meets specific functional and technical requirements, review its code for logic errors, and refine the implementation until it meets industry standards.

In a professional setting, you rarely write every line of code from scratch anymore. You write specs, you review PRs (Pull Requests), and you integrate libraries.

Think of this project like a ticket you might receive at a startup:

> "We need a lightweight internal tool to help new hires memorize our server acronyms. It needs to run in the terminal, load data from JSON, and have different quiz modes. The code needs to be clean so we can extend it later."

## Your Workflow

1. **Decompose**: Break the requirements below into small, logical prompts.
2. **Generate**: Feed these prompts to your AI agent.
3. **Review**: Does the code look right? Is it hallucinating imports? Does it handle errors?
4. **Refine**: Ask the AI to refactor specific parts (e.g., "Extract the quiz logic into a separate class").
5. **Verify**: Build and run tests.

## The Specifications

You must produce an application that meets the following criteria.

1. Functional Requirements (What the app does)

   - **Data Ingestion**:
     - The app must load flashcards from a JSON file.
     - It must validate the JSON structure. If the file is missing or malformed, the app should crash gracefully with a helpful error message, not a stack trace.
   - **The Quiz Loop**:
     - Present the "Front" of the card to the user.
     - Accept text input for the answer.
     - Compare input to the "Back" of the card (case-insensitive).
     - Provide immediate feedback (Correct/Incorrect).
   - **Quiz Modes**:
     - Sequential: Go through cards from 1 to N.
     - Random: Shuffle the deck.
     - Adaptive: This is the challenge feature. The app should prioritize cards the user previously got wrong.
   - **Session Stats**:
     - At the end of a quiz, show a summary table: Total Questions, Accuracy %, and a list of terms the user missed.

2. Technical Requirements

    - **Architecture**:
      - The code must be modular. Do not submit a single main.py file. Separation of concerns is required (e.g., data_loader.py, quiz_engine.py, ui.py).
    - **Design Patterns**:
      - Use the Strategy Pattern for the Quiz Modes.
      - Why? Because Sequential, Random, and Adaptive are different algorithms for the same task (selecting the next card). This allows you to easily add a "Spaced Repetition" mode later without rewriting the whole app.
    - **Type Safety**:
      - All functions must have Python Type Hints.
    - **Testing**:
      - The project must include a test suite (using pytest).
      - You need at least 80% code coverage.

## Deliverables

You will submit a GitHub repository containing:

1. Source Code: The generated and refined Python source code.
2. Test Suite: A tests/ directory with passing tests.
3. Prompt Log: A text file (prompts.md) documenting the specific prompts you gave the AI to get the desired result.
4. README.md: Instructions on how to install dependencies and run the app.

## Assessment

Your project will be assessed against a rubric on the following pages. Check the rubric before you start your project, and check it frequently throughout the development of your project to make sure you are completing all of the rubric criteria. Check your project against the rubric before submission.

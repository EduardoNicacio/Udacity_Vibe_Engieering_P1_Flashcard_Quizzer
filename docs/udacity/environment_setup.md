# Environment Setup

## Project Starter Github Repository

<https://github.com/udacity/cd14602-project-starter/tree/main/project>

To succeed in this project, you must manage two distinct environments: your **AI Assistant** (the builder) and the **Python Runtime** (the construction site).

## 1. The AI Development Stack

This is the layer where you will spend most of your time. You are not writing code manually; you are directing an AI agent to write it for you.

- **Primary Tool**: You must have a CLI-based AI agent installed and authenticated.
- Recommended: `Claude Code` or `Gemini CLI`. A Claude Code Workspace and access is provided for you.
- Alternative: AI-integrated IDEs (Cursor, VS Code with Copilot Workspace) are acceptable, provided they allow for terminal-based command execution.
- **API Access**: ensure you have valid API keys (e.g., Anthropic API Key, Google AI Studio Key) exported in your terminal session so your agent can communicate with the LLM. The provided Claude Code workspace includes an Anthropic API Key.
- _Tip_: Test your agent before starting. Run `claude "Hello, are you ready to code?"` or the equivalent Gemini command to verify connectivity.

## 2. The Target Runtime (The Construction Site)

This is the environment where your generated application will live. You must instruct your AI agent to target these specific versions and constraints.

- **Language**: Python 3.10 or higher.
- **Package Management**: Standard pip (do not use Poetry or Pipenv for this specific assignment to keep the agent's context simple).
- **Virtualization**: venv module.

## 3. Setup Instructions

### Step A: Prepare the Workspace

Before prompting the AI, set up the directory structure.

1. **Create your project folder**:

    ```bash
    mkdir flashcard-quizzer
    cd flashcard-quizzer
    ```

2. **Initialize the Python Virtual Environment**: Even though the AI writes the code, you control the environment. Isolate your dependencies immediately.

```bash
# MacOS/Linux

python3 -m venv venv
source venv/bin/activate

# Windows

python -m venv venv
venv\Scripts\activate
```

### Step B: Define the "Definition of Done" for the AI

You are expected to configure your AI agent to check its own work. When you prompt your agent to generate code, require it to install and run the following quality assurance tools:

- `pytest`: For running the test suite.
- `black`: For enforcing code formatting.
- `mypy`: For static type checking.

## 4. Running the Generated Application

Once your AI agent has successfully generated the code, you should be able to interact with the application using standard CLI commands.

**Success Criteria**: Your project is correctly configured if you can execute the following commands in your terminal without errors:

```bash
# The Help Command (Must display all available flags)
python main.py --help

# The Quiz Loop (Standard operation)
python main.py --mode sequential --file data/glossary.json
```

# Workspace Instructions

## Accessing Your Claude Code Workspace

We have provided a cloud-based development environment pre-configured with Claude Code, an advanced AI coding agent that runs directly in your terminal for you to do the course project. Use this workspace for all of the course exercises. This workspace connects you to powerful models via AWS Bedrock, ready for you to start building.

1. Start the Lab

   - In the classroom, click the "Cloud Resources" tab.
   - The lab interface will open in a new browser tab.
   - Select "Start Lab" to begin provisioning your environment.

2. Wait for Status Checks

   - Look for the status indicators next to "VS Code" and "AWS".
   - When these dots turn green, your environment is fully ready for use.

3. Launch Claude Code

   Inside the VS Code interface:

    1. Open a terminal by selecting View > Terminal from the top menu bar.
    2. At the command prompt, type Claude and press Enter.
    3. You can now interact with the AI agent to plan, generate, and refine your code!

## Lab Token Usage Limits and Thresholds

- Mindful Usage: You do not have access to unlimited tokens and Anthropic models in the workspace. To keep this powerful technology available to all learners, the workspace operates with token usage thresholds and limits. We encourage you to plan your prompts thoughtfully; this helps you stay within the limits, maintains your lab access, and often leads to higher-quality code results.
- Model Availability: Claude Code uses cutting-edge models hosted on AWS Bedrock. Occasionally, these models may experience short periods of high demand. If you see an error message about model availability or capacity, don't worry—just wait a moment and try your command again.
- Deactivation: If you experience deactivation due to token usage, you will need to contact Udacity support to investigate and reactivate the Claude Code workspace.

## Managing Packages and Your Workspace Environment

### Your Workspace is a Clean Slate

You are working in an environment that simulates a fresh production server or a new local computer. Aside from Python, no external libraries are pre-installed. This is intentional—it gives you the freedom to build exactly what you need without conflicts.

### You Have Full Control

If an exercise requires libraries like pandas, pytest, or requests, they are not missing; you simply haven't installed them yet. You have full permissions to install whatever packages you need to complete your work.

#### The Best Way: Let Your Coding Assistant Handle It

In this course, your goal is to act as the architect while the AI acts as the builder. This applies to your environment, too. You don't need to manually type pip install commands unless you prefer to.

### Prompt Claude to configure the environment for you:

- "I'm starting the phantom dependency exercise. Please look at the code, identify the required libraries, and install them for me."
- "Create a virtual environment for this project and install the dependencies listed in requirements.txt."
- If you see a ModuleNotFoundError, just tell Claude: "I'm getting a missing module error. Please fix the environment."

By delegating these tasks to your AI coding assistant, you focus on the engineering decisions while the AI handles the configuration details.

## Accessing the Claude Code Workspace

A user interface for managing VM resources in cloud computing, displaying a message that the cloud resource is inactive. There are options to 'Start Cloud Resource' and 'Open Cloud Console', along with a reminder to monitor budget allocation.

Click on "Cloud Resources" and "Start Cloud Resources" then "Open Cloud Console" to access the Claude Code Workspace

### Starting and Ending the Workspace Lab

Buttons to control a lab simulation: 'Start Lab' with a play icon, 'End Lab' as a solid square, and a 'Reset' button featuring a circular arrow.

Remember to start and end the lab in the workspace

### Starting Claude Code in the VS Code Terminal

A terminal window in Visual Studio Code, displaying the prompt 'labsuser@vscode:~$' with 'claude' typed in the command line.

In the VS Code menu, click on "View" then choose "Terminal". Type "claude" in the terminal to start Claude Code.

### Using Claude Code in the VS Code Terminal

A interface welcoming users to Claude Code, featuring options for text styles: 'Dark mode' is selected as the first choice, followed by 'Light mode' and other variations. A code preview shows a function named 'greet' with a highlighted change from 'Hello, World!' to 'Hello, Claude!'. The interface includes menu tabs labeled 'PROBLEMS', 'OUTPUT', 'DEBUG CONSOLE', 'TERMINAL', and 'PORTS'.

Claude Code is a CLI tool, follow the prompts to begin using the CLI in the terminal.

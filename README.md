# Letta Sourcing Agent

Example sourcing agent built with Letta and the 11x API.

## Project Setup

This guide explains how to set up a virtual environment for this project, install dependencies, and run the tool scripts.

### Prerequisites

Before you begin, ensure you have Python and pip installed on your system.

- **Python:** Download and install Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  - Verify the installation by opening your terminal or command prompt and typing `python --version` or `python3 --version`.
- **pip:** pip is the package installer for Python and is usually included with Python installations (version 3.4+)

### Setup Instructions

1.  **Create a virtual environment:**
    Navigate to the project's root directory in your terminal. Python 3 includes a built-in module called `venv` for creating virtual environments. Run the following command:

    ```bash
    python3 -m venv .venv
    ```

    _(Note: Depending on your system, you might need to use `python` instead of `python3`. If you previously used `pip install virtualenv` and encountered an `error: externally-managed-environment`, this is the recommended approach as it avoids modifying the system's Python installation.)_

    This command creates a directory named `.venv` containing the Python interpreter and libraries specific to this project. Using `.venv` (starting with a dot) is a common convention for virtual environment directories.

2.  **Activate the virtual environment:**

    - On macOS:
      ```bash
      source .venv/bin/activate
      ```
      Your terminal prompt should now change (often showing `(.venv)` at the beginning), indicating the virtual environment is active.

3.  **Install dependencies:**
    With the virtual environment active, install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    If you're developing for this project, also install development dependencies:

    ```bash
    pip install -r requirements-dev.txt
    ```

## Environment Variables

This project requires setting up an environment variable for authentication with the 11x API:

1. **Set the API key environment variable:**

   ```bash
   export API_KEY="<your-api-key>"
   ```

   This sets the API key for the current terminal session only. To make it persistent:

   - For Bash users (add to `~/.bashrc` or `~/.bash_profile`):

     ```bash
     echo 'export API_KEY="<your-api-key>"' >> ~/.bash_profile
     source ~/.bash_profile
     ```

   - For Zsh users (add to `~/.zshrc`):

     ```bash
     echo 'export API_KEY="<your-api-key>"' >> ~/.zshrc
     source ~/.zshrc
     ```

   - For Windows users (PowerShell):
     ```powershell
     [Environment]::SetEnvironmentVariable("API_KEY", "<your-api-key>", "User")
     ```

## Running a Tool Script

Once the setup is complete and the virtual environment is active, you can run any of the Python scripts located in the `tools/` directory.

For example, to run the script that executes a search query:

```bash
python tools/execute_people_search_query.py
```

_(Note: You might need to provide arguments or modify the script for specific usage, depending on the script's requirements. Refer to the script's internal documentation or code for details.)_

## Linting

This project uses `flake8` for linting Python code. To check the code for style issues and errors:

1.  **Install development dependencies (if not already installed):**
    Ensure your virtual environment is active, then run:

    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Run flake8:**
    From the project root directory, run:
    ```bash
    flake8 .
    ```
    This command will check all Python files in the current directory and subdirectories, respecting the exclusion rules defined in the `.flake8` configuration file.

## Exiting and Cleaning Up

1.  **Deactivate the virtual environment:**
    Simply run the following command in your terminal:

    ```bash
    deactivate
    ```

    The `(venv)` prefix will disappear from your prompt.

2.  **Remove the virtual environment (optional):**
    If you no longer need the virtual environment, you can delete its directory:
    - On macOS:
      ```bash
      rm -rf venv
      ```

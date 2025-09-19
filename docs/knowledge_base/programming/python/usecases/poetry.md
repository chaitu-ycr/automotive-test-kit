# ✒️ Usecase: Managing Projects with `Poetry`

For a long time, managing Python projects involved a messy combination of tools: `venv` for virtual environments, a `requirements.txt` file for dependencies (which could easily become outdated), and `setup.py` for packaging. It worked, but it was clunky.

**Poetry** is a modern, all-in-one tool that solves these problems. It handles dependency management, virtual environment creation, and packaging, all through one consistent interface and a single configuration file: `pyproject.toml`. It makes your projects more professional, reproducible, and easier to manage.

## 🗺️ A Mind Map of the Poetry Workflow

The lifecycle of a Poetry project is simple and intuitive.

```mermaid
graph TD
    A[Start] --> B(poetry new my-project);
    B --> C{Add Dependencies};
    C -- `poetry add requests` --> D;
    C -- `poetry add pytest --group dev` --> D;
    D(pyproject.toml & poetry.lock);
    D --> E(poetry install);
    E --> F{Run Code};
    F -- `poetry run python app.py` --> G;
    F -- `poetry shell` --> G;
    G(Develop & Test);
    G --> H(poetry build);
    H --> I(poetry publish);
    I --> J[End];

    style D fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 🤔 What Is Poetry?

Poetry is a tool for Python dependency management and packaging. It helps you declare the libraries your project depends on, manages the installation of those libraries in isolated virtual environments, and helps you build and publish your project for others to use.

## ✨ Why Is Poetry So Useful?

*   **All-in-One Tool:** It replaces the need for `venv`, `pip`, `requirements.txt`, and `setup.py`. Everything is managed through the `poetry` command and the `pyproject.toml` file.
*   **Deterministic Builds:** Poetry creates a `poetry.lock` file that records the *exact* versions of all your dependencies. This guarantees that anyone who runs `poetry install` will have the exact same environment, eliminating "it works on my machine" problems.
*   **True Dependency Resolution:** Unlike `pip`, Poetry has a true dependency resolver. It will figure out a compatible set of versions for all your dependencies and their sub-dependencies, preventing version conflicts.
*   **Clear Separation of Dependencies:** It keeps your main dependencies separate from your development dependencies (like `pytest` or `black`), so your production environment stays clean.

---

## 🚀 How Do I Use Poetry?

Let's walk through setting up and managing a new project.

### 1. Installation

It's recommended to install Poetry using its official installer to isolate it from your projects.
```bash
# For macOS / Linux / WSL
curl -sSL https://install.python-poetry.org | python3 -

# For Windows (in PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python3 -
```

### 2. Starting a New Project

The `poetry new` command creates a standardized, professional project structure.

```bash
poetry new my-awesome-project
```
This creates a folder `my-awesome-project/` with a `pyproject.toml` file, a `README.md`, a tests folder, and a source folder.

### 3. The `pyproject.toml` File

This is the heart of your project. It's where you define everything about your project.

```toml
[tool.poetry]
name = "my-awesome-project"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.9" # This project is compatible with Python 3.9 and later

[tool.poetry.group.dev.dependencies]
pytest = "^7.0" # A development-only dependency
```

### 4. Adding and Installing Dependencies

You should never manually edit the `dependencies` section. Let Poetry do it for you.

**To add a library your project needs to run (like `requests`):**
```bash
poetry add requests
```

**To add a library only for development (like `pytest`):**
```bash
poetry add pytest --group dev
```
These commands will automatically find a compatible version, add it to `pyproject.toml`, and update the `poetry.lock` file.

**To install all dependencies from the lock file:**
This is what a new collaborator would run after cloning your project.
```bash
poetry install
```

### 5. Running Your Code

Poetry automatically creates and manages a virtual environment for your project. To run your code inside this environment, you have two options:

**1. Use `poetry run`:**
This executes a single command inside the project's environment.
```bash
poetry run python my_awesome_project/main.py
```

**2. Activate the virtual environment with `poetry shell`:**
This spawns a new shell inside the environment, so you can run commands directly.
```bash
poetry shell
# Now you are in the virtual environment
# You can just run:
python my_awesome_project/main.py
exit # to leave the shell
```

### 6. Building and Publishing

When your project is ready to be shared, Poetry makes it simple.

**To build your project into distributable packages:**
```bash
poetry build
```
This creates a `.tar.gz` (source archive) and a `.whl` (wheel) file in a new `dist/` directory.

**To publish your package to PyPI (the Python Package Index):**
```bash
# You'll need to configure your PyPI credentials first
poetry publish
```
Poetry provides a robust, modern workflow that takes the guesswork out of managing Python projects.

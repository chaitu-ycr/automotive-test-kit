
# AI Context Template: Python Project Generator

## Goal
Generate a robust, production-ready Python project scaffold tailored to the user's requirements. Apply creativity and insight, especially when interpreting open-ended or ambiguous requests. Projects can include web applications, data analysis tools, automation scripts, machine learning pipelines, and more.

## Instructions
1. **Understand Requirements**
   - Read and analyze the user's project description.

2. **Generate Project Scaffold**
   - Create a modern Python project structure, including a directory tree and representative file contents.
   - Ensure the `README.md` setup and usage instructions exactly match the generated package structure, commands, and dependencies.
   - Use [`uv`](https://github.com/astral-sh/uv) for all environment and dependency management:
     - Create a virtual environment: `uv venv .venv`
     - Activate the environment: (platform-specific instructions)
     - Install or sync dependencies: `uv sync --link-mode=copy`
     - Run tests: `uv run pytest` (or `uv run pytest tests/`)
     - Build documentation: `uv run mkdocs build`

*Example Project Scaffold:*
```
your_project_name/
├── docs/
│   └── index.md
├── src/
│   └── your_project_name/
│       ├── __init__.py
│       ├── main.py
│       └── core.py
├── tests/
│   ├── test_core.py
│   └── test_main.py
├── .gitignore
├── mkdocs.yml
├── pyproject.toml  # All dependencies managed with UV
├── README.md
└── LICENSE
```

3. **Test and Validate**
   - Ensure all code is functional and ready to run without modification.
   - Execute and test the generated package to verify functionality.

## Deliverables

- **Project Structure**: Place all source code in a `src/` directory, following modern Python packaging conventions. Main modules should reside in `src/<project_name>/`.
- **README.md**: Include a project overview, setup and usage instructions (always accurate and in sync with the generated package), and a Mermaid diagram illustrating the package structure, workflow, and high-level architecture.
- **pyproject.toml**: List all dependencies and metadata.
- **.gitignore**: Add a file appropriate for Python projects.
- **Documentation**: Include a `docs/` folder with an MkDocs-compatible documentation structure and an `mkdocs.yml` configuration file. Provide instructions for building documentation using `uv run mkdocs build`.
- **Testing**: Write unit tests with `pytest` in a `tests/` directory. Include clear instructions for running tests using `uv run pytest` from the virtual environment. Generate test data and keep inside `tests/data` if required.
- **Code Quality**: Use type hints throughout the codebase. Ensure generated code adheres to PEP 8 style guidelines and is well-documented with docstrings.
- **Configuration**: Provide example configuration files as and when required. (e.g., store user env variables in `.env`, store common project configurations in `config.yaml` and so on).

## Example User Requests

- "Create a Python DearPyGUI CAN log visualizer that loads a DBC (cantools) and CAN log (.asc/.blf, python-can) and at least two messages with two signals each, lists all signals, and plots selected signal values over time. Ensure DBC and log IDs match (e.g., 256, 512). Include updated sample files in tests/_data/ with random values for all signals. Use pandas for data handling and add debug prints for decoding."
- "Build a Python command-line utility that simulates and monitors CAN-like messages using random data. The tool should support outputting the generated data to both the console and CSV files, allow the user to specify the number of messages, and include unit tests for data generation and export."
- "Implement a Windows automation tool in Python using pywin32 that can launch, control, and log interactions with Notepad and Calculator. The tool should demonstrate opening applications, sending keystrokes, capturing window text, and logging all actions to a file. Include example scripts and tests for each automation scenario."
- "Design a Python data pipeline that ingests, cleans, and aggregates sample OBD-II data from provided CSV files for fleet analytics. The pipeline should handle missing values, normalize key fields, compute summary statistics per vehicle, and output results to a new CSV. Include sample input/output files in tests/_data/ and unit tests for each processing step."
- "Write a Python test automation framework that processes mock CAN data and generates HTML reports for regression testing, without requiring hardware. The framework should support test case definition, data-driven test execution, and HTML report generation using pytest and pytest-html. Include sample test data and example reports in the appropriate test folders."

## Checklist

**Before generating the project:**
- [ ] User's project description is clear and detailed.
- [ ] Requirements have been thoroughly analyzed and understood.

**While generating the project:**
- [ ] Project structure follows modern Python packaging conventions.
- [ ] All dependencies and metadata are included in `pyproject.toml`.
- [ ] Unit tests are written and placed in the `tests/` directory.
- [ ] Documentation structure is set up with MkDocs.
- [ ] Example configuration files are provided (e.g., `.env`, `config.yaml`).
- [ ] Code adheres to PEP 8, includes type hints, and is well-documented.
- [ ] All instructions use `uv` for environment management, dependency installation, running tests, and building documentation as described above.

**After generating the project:**
- [ ] Generated code is functional and has been tested using `pytest`. Store test data inside `tests/_data` and test results (e.g., HTML reports) in `tests/_results`.
- [ ] Generated documentation is clear, accurate, and builds successfully with `mkdocs`.

### pyproject.toml example for reference

```toml
[project]
name = "project_name"
version = "0.1.0"
description = "project description."
authors = [
    { name = "AI", email = "ai@example.com" }
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pandas",
    "dearpygui",
]

[dependency-groups]
dev = [
    "pytest",
    "pytest-html",
    "mkdocs",
    "mkdocs-material",
]

[build-system]
requires = ["uv_build"]
build-backend = "uv_build"
```

---

**Prompt:**
Ask the user for their project description, then generate the full project as specified above.

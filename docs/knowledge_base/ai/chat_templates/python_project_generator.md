# 🐍 Python Project Generator
*A modular, AI-ready template for creating production-quality Python projects.*

---

### **Metadata**
- **Version:** 1.0.0
- **Author:** automotive-test-kit
- **Tags:** python, cli, api, gui, web

---

### **How to Use**
1. **Follow each section sequentially, providing input where prompted (e.g., "Your turn").**
2. **Type "continue" to advance. The generator adapts to your choices.**
3. **All packaging, build, sync, venv, and dependency management must use [Python UV](https://github.com/astral-sh/uv) and `pyproject.toml`:**
	 - If UV is not installed, run: `pip install uv`
	 - Do not use pip, poetry, conda, requirements.txt, or manual edits for project management.
	 - Manage all dependencies via UV commands; do not manually edit `pyproject.toml`.
	 - Example UV commands:
		 - `uv venv .venv` (create virtual environment)
		 - `uv init --build-backend uv_build --package your-package-name` (initialize packaged application)
		 - `uv add httpx` (add dependency; use `--dev`, `--group`, or `--optional` for alternatives)
		 - `uv remove httpx` (remove dependency)
		 - `uv sync` (sync environment)
		 - `uv build` (build source and binary distributions)
	 - Reference: [UV GitHub](https://github.com/astral-sh/uv), [UV Docs](https://docs.astral.sh/uv/)
	 - **Why UV?** UV is a modern, fast, and reproducible Python packaging tool. All dependency changes must be made via UV commands.

---

## 1. Project Overview
**Describe your project in 1-2 sentences.**
*Example: "A Python CLI tool to monitor a folder and back up new files to cloud storage."*

**Your turn:**
> *Your project description here*

---

## 2. Essential Project Details
**Fill in the key details for your project.**
- **Main Goal:** (e.g., "REST API for a book collection")
- **Python Package Manager:** **UV (required, with pyproject.toml for dependencies; install with `pip install uv` if not present)**
- **Target Platforms:** (e.g., Windows, Linux, macOS, cloud)
- **Python Version:** (e.g., 3.11+)
- **Key Dependencies:** (e.g., FastAPI, SQLAlchemy, requests, pandas)
- **Testing Framework:** (e.g., pytest)
- **Linting & Formatting:** (e.g., ruff, black)
- **Documentation:** (e.g., MkDocs)
- **CI/CD:** (e.g., GitHub Actions, Jenkins)
- **License:** (e.g., MIT)
- **Author:** (e.g., "automotive-test-kit")

**Your turn:**
> *Your project details here (Note: Use only Python UV and pyproject.toml for all packaging, build, sync, venv, and dependency management. If UV is not installed, run `pip install uv`. Use UV commands for all dependency changes; do not manually edit pyproject.toml.)*

---

## 3. Project Structure
**A project structure will be suggested based on your inputs. Review and request changes.**
*Example Structure:*
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
│   └── test_core.py
├── .gitignore
├── mkdocs.yml
├── pyproject.toml  # All dependencies managed with UV
├── README.md
└── LICENSE
```

**Your turn:**
> *Request any changes to the structure, or type "continue".*

---

## 4. Final Review
**Review the generated configuration and files one last time before completion.**
- [ ] Project overview and details are correct.
- [ ] Project structure is finalized.
- [ ] Build, dependency, and tooling configurations are confirmed.
- [ ] CI/CD workflow is ready.

**Your turn:**
> *Type "done" to complete the generation process.*

---

## 5. Next Steps
- Implement the core logic in the `src` directory.
- Write comprehensive tests in the `tests` directory.
- Update the documentation in the `docs` directory.
- Use only Python UV for all packaging, build, sync, venv, and dependency management.
	- Manage all dependencies via UV commands; do not manually edit pyproject.toml.
	- If UV is not installed, run: `pip install uv`
	- Example UV commands:
		- `uv venv .venv`
		- `uv init --build-backend uv_build --package your-package-name`
		- `uv add httpx`
		- `uv remove httpx`
		- `uv sync`
		- `uv build`
- Push your initial commit to trigger the CI/CD pipeline.

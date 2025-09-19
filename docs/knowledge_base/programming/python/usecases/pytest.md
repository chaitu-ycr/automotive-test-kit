# 🧪 Usecase: Writing Tests with `pytest`

Writing code is one thing, but how can you be sure it actually works correctly? And more importantly, how can you be sure it *keeps* working correctly after you make changes? The answer is **automated testing**, and `pytest` is the most popular, powerful, and Pythonic framework for doing it.

`pytest` makes writing tests fun. It has a simple, clean syntax and a powerful feature set that scales from small scripts to complex applications.

## 🗺️ A Mind Map of `pytest`'s Core Features

`pytest` is built around a few powerful, easy-to-use concepts.

```mermaid
mindmap
  root((pytest))
    --> Test Discovery
      --> Finds `test_*.py` or `*_test.py` files
      --> Runs functions prefixed with `test_`
    --> Simple `assert` Statements
      --> `assert expected == actual`
      --> No need for `self.assertEqual(...)`
      --> Provides detailed failure messages
    --> Fixtures (`@pytest.fixture`)
      --> Reusable setup/teardown code
      --> Manages test data and resources
      --> Injected into tests as arguments
    --> Markers (`@pytest.mark`)
      --> `@pytest.mark.parametrize`: Run one test with many inputs
      --> `@pytest.mark.skip`: Skip a test
      --> `@pytest.mark.xfail`: Expect a test to fail
```

---

## 🤔 What Is `pytest`?

`pytest` is a testing framework that allows you to write small, readable tests. It's designed to be easy to get started with, yet powerful enough to handle complex testing scenarios. It automatically discovers your test files and functions, runs them, and provides detailed reports on their success or failure.

## ✨ Why Is `pytest` So Popular?

*   **Simple Syntax:** It uses plain `assert` statements instead of the boilerplate `self.assertEqual()` or `self.assertTrue()` found in other frameworks. This makes tests shorter and more readable.
*   **Powerful Fixtures:** Fixtures are a clean and modular way to provide data and resources to your tests (like a database connection or a sample dataset). This avoids code duplication and makes tests easier to manage.
*   **Rich Ecosystem:** It has hundreds of plugins that extend its functionality for things like web testing (`pytest-selenium`), code coverage (`pytest-cov`), and asynchronous code (`pytest-asyncio`).
*   **Excellent Failure Reporting:** When an `assert` fails, `pytest` gives you a detailed report showing the exact values of the variables involved, which makes debugging much faster.

---

## 🚀 How Do I Write Tests with `pytest`?

Let's write some tests for a simple set of functions.

### 1. Installation

First, you need to install the library. It's usually installed as a development dependency.
```bash
# Using pip
pip install pytest

# Or with Poetry
poetry add pytest --group dev
```

### 2. The Code to Test

Let's imagine we have a `utils.py` file with some functions we want to test.
```python
# utils.py
def add(a, b):
  return a + b

def is_even(n):
  return n % 2 == 0
```

### 3. Writing Basic Tests

Create a new file named `test_utils.py`. `pytest` will automatically find it. Test functions must start with `test_`.

```python
# test_utils.py
from utils import add, is_even

def test_add():
  """Tests the add function with positive numbers."""
  assert add(2, 3) == 5

def test_add_negative():
  """Tests the add function with negative numbers."""
  assert add(-1, -1) == -2

def test_is_even():
  """Tests the is_even function."""
  assert is_even(10) is True
  assert is_even(7) is False
```

To run your tests, just navigate to your project's root directory in the terminal and run:
```bash
pytest
```
`pytest` will discover and run your tests, giving you a clear pass/fail report.

### 4. Reusing Setup Code with Fixtures

Imagine you have a complex object that you need for multiple tests. Instead of creating it in every test, you can use a fixture.

```python
# test_data.py
import pytest

@pytest.fixture
def sample_data():
  """A fixture that provides a sample list for testing."""
  print("\n(Creating sample_data fixture...)")
  return [10, 20, 30]

def test_sum(sample_data):
  """Tests the sum of the sample data."""
  assert sum(sample_data) == 60

def test_length(sample_data):
  """Tests the length of the sample data."""
  assert len(sample_data) == 3
```
`pytest` will automatically run the `sample_data` function and "inject" its return value into any test that accepts it as an argument.

### 5. Testing Multiple Scenarios with `parametrize`

What if you want to run the same test with many different inputs? You can use the `@pytest.mark.parametrize` marker.

```python
# test_utils.py
import pytest
from utils import is_even

@pytest.mark.parametrize("number, expected_result", [
    (2, True),
    (7, False),
    (0, True),
    (-1, False),
    (-10, True)
])
def test_is_even_many_cases(number, expected_result):
  """Tests the is_even function with multiple inputs."""
  assert is_even(number) == expected_result
```
`pytest` will run this test five times, once for each tuple in the list, substituting `number` and `expected_result` each time. This is a powerful way to write comprehensive tests with very little code.

### 6. Testing for Exceptions

You can easily test that your code raises an expected error using `pytest.raises`.

```python
# test_errors.py
import pytest

def test_division_by_zero():
  """Tests that dividing by zero raises a ZeroDivisionError."""
  with pytest.raises(ZeroDivisionError):
    result = 1 / 0
```
The test will pass only if a `ZeroDivisionError` is raised inside the `with` block.

Writing tests with `pytest` provides a safety net that allows you to refactor and add new features with confidence, knowing that you haven't broken existing functionality.

# 📝 016: Documenting Your Code

Writing code that works is only half the battle. Writing code that others (and your future self!) can understand, use, and maintain is just as important. Good documentation is the key to turning a simple script into a professional, long-lasting piece of software.

In Python, there are two main ways to document your code: **comments** and **docstrings**.

## 🗺️ A Mind Map of Python Documentation

Think of documentation as having two different audiences: one for the person reading your source code, and one for the person *using* your code.

```mermaid
mindmap
  root((Code Documentation))
    --> Comments (`#`)
      --> **For the code reader**
      --> Explains the *why* and the *how*
      --> Ignored by Python
      --> Use for complex logic or non-obvious decisions
    --> Docstrings (`"""..."""`)
      --> **For the code user**
      --> Explains the *what* and the *how to use*
      --> Attached to the object (`__doc__`)
      --> Used by tools like `help()` and Sphinx
      --> Belongs at the start of a module, class, or function
```

---

## 🤔 What's the Difference? Comments vs. Docstrings

*   **Comments (`#`) are for the maintainers.** They are notes written in the source code to help developers who are reading it understand *why* a particular piece of code is written the way it is. They are completely ignored by the Python interpreter.
*   **Docstrings (`"""..."""`) are for the users.** They are strings that describe how to *use* your module, class, or function. They are part of the code itself and can be accessed at runtime. This allows tools like `help()` and automatic documentation generators to show users how your code works without them needing to read the source.

## ✨ Why Is Good Documentation So Important?

*   **It's a gift to your future self:** In six months, you will have forgotten why you made certain decisions. Good comments and docstrings will save you hours of deciphering your own work.
*   **Collaboration:** It's essential for teamwork. It allows other developers to understand and use your code without having to ask you questions constantly.
*   **Clarity of Thought:** The act of writing documentation often forces you to think more clearly about your code's design and purpose.
*   **Professionalism:** Well-documented code is a hallmark of a professional developer.

---

## 🚀 How to Document Your Code

Let's look at how to write effective comments and docstrings.

### 1. Writing Effective Comments (`#`)

The best comments explain the **why**, not the **what**.

**A bad, useless comment (restates the obvious):**
```python
# Add 1 to x
x = x + 1
```

**A good, helpful comment (explains the reasoning):**
```python
# We need to offset the index by 1 to account for the header row.
x = x + 1
```

Use comments to clarify tricky parts of your code, explain your intent, or leave notes for future improvements (e.g., `# TODO: Refactor this to be more efficient`).

### 2. Writing High-Quality Docstrings (`"""..."""`)

A docstring is a string literal that occurs as the first statement in a module, function, class, or method definition. The most common convention is the [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) or the [NumPy/SciPy style](https://numpydoc.readthedocs.io/en/latest/format.html).

Here's a great structure to follow for a function docstring:

```python
def calculate_average(numbers: list[float]) -> float:
  """Calculates the average of a list of numbers.

  This function takes a list of numbers and returns their arithmetic mean.
  It handles the case of an empty list by returning 0.0.

  Args:
    numbers: A list of floats or integers.

  Returns:
    The float average of the numbers, or 0.0 if the list is empty.

  Raises:
    TypeError: If the list contains non-numeric types.

  Example:
      >>> calculate_average([1, 2, 3])
      2.0
  """
  if not numbers:
    return 0.0
  return sum(numbers) / len(numbers)
```

**Key parts of a great docstring:**
1.  **A one-line summary:** A quick, imperative statement (e.g., "Calculate the average...").
2.  **A more detailed description (optional):** Explain the function's behavior in more detail.
3.  **`Args:` section:** List each parameter, its type, and what it represents.
4.  **`Returns:` section:** Describe the return value and its type.
5.  **`Raises:` section (optional):** List any exceptions that the function might raise.

You can access this docstring at any time using the `help()` function or the `__doc__` attribute:
```python
help(calculate_average)
# or
print(calculate_average.__doc__)
```

Writing good documentation might seem like extra work, but it's one of the most valuable investments you can make in your code.

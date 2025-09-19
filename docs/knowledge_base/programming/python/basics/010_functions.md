# 🧩 010: Creating Reusable Code with Functions

So far, we've been writing scripts that run from top to bottom. But what if you need to perform the same action multiple times? For example, greeting a user. You could copy and paste `print("Hello, user!")`, but if you need to change the message, you'd have to change it everywhere. This is where **functions** come in.

A function is a named, reusable block of code that performs a specific task. Think of it as a recipe: you define it once, and you can use it as many times as you want.

## 🗺️ A Mind Map of a Python Function

Let's break down the anatomy of a function.

```mermaid
mindmap
  root((Function))
    --> Definition
      --> `def` keyword
      --> Function name (e.g., `greet`)
      --> Parameters (e.g., `name`) in parentheses `()`
      --> Colon `:`
    --> Body
      --> Indented code block
      --> The logic that performs the task
    --> Docstring
      --> `"""Explains what the function does."""`
    --> Return Value
      --> `return` keyword
      --> Sends a result back to the caller
      --> Optional (returns `None` if omitted)
```

---

## 🤔 What Is a Function?

A function is a self-contained block of code that you can "call" by name to execute it. Functions can optionally take in data (as **parameters**) and send data back (as a **return value**).

Here's a simple function that greets a person:
```python
# --- Function Definition ---
def greet(name):
  """This function takes a name and prints a greeting."""
  print(f"Hello, {name}! Welcome to the world of functions. 👋")

# --- Calling the Function ---
greet("Alice")
greet("Bob")
```
We defined the `greet` logic once and called it twice with different data.

## ✨ Why Are Functions So Important?

Functions are a cornerstone of well-written code. They allow you to practice the **DRY** principle: **D**on't **R**epeat **Y**ourself.

*   **Reusability:** Write a piece of logic once and use it anywhere in your application.
*   **Modularity:** Break down a large, complex program into smaller, manageable, and understandable pieces. It's easier to work on `calculate_tax()` than a giant script that does everything.
*   **Abstraction:** You don't need to know *how* a function works to use it. You just need to know its name and what inputs it needs. The `print()` function is a perfect example—you use it all the time without needing to know the complex details of how it displays text on the screen.
*   **Maintainability:** If you need to fix a bug or update logic, you only have to do it in one place: inside the function.

---

## 🚀 How Do I Build Functions?

Let's explore the key components of building and using functions.

### 1. Parameters vs. Arguments

This is a common point of confusion, but the distinction is simple:
*   **Parameter:** The variable listed inside the function's parentheses during definition (e.g., `name` in `def greet(name):`). It's a placeholder.
*   **Argument:** The actual value that is sent to the function when it is called (e.g., `"Alice"` in `greet("Alice")`). It's the real data.

### 2. Return Values: Getting Data Back

Many functions perform a calculation and need to send a result back. The `return` statement does this. When `return` is executed, the function stops immediately and sends the value back to where it was called.

```python
def add(a, b):
  """This function adds two numbers and returns the result."""
  result = a + b
  return result

# The value returned by the function is stored in the 'sum_result' variable
sum_result = add(5, 3)
print(f"The sum is: {sum_result}") # The sum is: 8
```
A function with no `return` statement implicitly returns `None`.

### 3. Different Types of Arguments

You can define arguments in several flexible ways:

*   **Positional Arguments:** The standard arguments that are matched based on their position. `add(5, 3)`
*   **Keyword Arguments:** You specify the argument by its parameter name, so the order doesn't matter. `add(b=3, a=5)`
*   **Default Arguments:** You can provide a default value for a parameter, making it optional when the function is called.

    ```python
    def greet(name="World"):
      print(f"Hello, {name}!")

    greet()       # Prints "Hello, World!"
    greet("Alice") # Prints "Hello, Alice!"
    ```

### 4. Advanced: `*args` and `**kwargs`

What if you don't know how many arguments will be passed to your function?

*   `*args`: Collects all extra positional arguments into a **tuple**.
*   `**kwargs`: Collects all extra keyword arguments into a **dictionary**.

```python
def show_everything(*args, **kwargs):
  print(f"Positional arguments (a tuple): {args}")
  print(f"Keyword arguments (a dictionary): {kwargs}")

show_everything(1, 2, "hello", name="Alice", age=30)
# Positional arguments (a tuple): (1, 2, 'hello')
# Keyword arguments (a dictionary): {'name': 'Alice', 'age': 30}
```

By mastering functions, you take a massive leap from just writing scripts to building well-structured, professional-grade programs.

# 🛡️ 012: Error and Exception Handling

No matter how good a programmer you are, things can go wrong. A user might enter text where you expect a number, a file you need might be missing, or a network connection could drop. If you don't prepare for these situations, your program will crash. **Exception handling** is how you build a robust program that can gracefully handle errors and continue running.

Think of it as a safety net for your code.

## 🗺️ A Mind Map of the `try...except` Block

This is the structure you'll use to catch and handle exceptions.

```mermaid
graph TD
    A[Start] --> B(try block);
    B -- No Exception --> D(else block);
    B -- Exception Occurs --> C{Matches an except block?};
    C -- Yes --> E(except block);
    C -- No --> F[Crash! 😱];
    D --> G(finally block);
    E --> G;
    G --> H[Continue Program];
```

---

## 🤔 What Are Exceptions?

An **exception** is an error that happens during the execution of a program. When Python encounters an error, it "raises" an exception, and if that exception isn't "handled," the program stops.

There are many built-in exception types for common errors:
*   `ValueError`: An operation receives an argument of the right type but an inappropriate value (e.g., `int("abc")`).
*   `TypeError`: An operation is performed on an object of an inappropriate type (e.g., `"2" + 2`).
*   `ZeroDivisionError`: You tried to divide by zero.
*   `FileNotFoundError`: You tried to open a file that doesn't exist.
*   `KeyError`: You tried to access a dictionary key that doesn't exist.

## ✨ Why Is Exception Handling So Important?

Writing `try...except` blocks is about moving from a fragile script to a resilient application.

*   **Prevents Crashing:** It's the difference between a program that crashes when something unexpected happens and one that handles the problem gracefully.
*   **User Experience:** You can provide friendly error messages to the user (e.g., "Invalid input, please enter a number") instead of showing them a scary traceback.
*   **Resource Management:** The `finally` block ensures that critical cleanup actions (like closing a file or a network connection) happen, no matter what.
*   **Reliability:** It allows your program to recover from non-critical errors and continue its work.

---

## 🚀 How Do I Handle Exceptions?

You use the `try...except...else...finally` block to manage exceptions.

### 1. The `try` and `except` Blocks

This is the most basic and common pattern.

```python
try:
  # 1. The code that might cause an error goes in the 'try' block.
  user_input = input("Please enter a number: ")
  number = int(user_input)
  result = 10 / number
  print(f"10 divided by your number is: {result}")

except ValueError:
  # 2. This block runs ONLY if a ValueError occurs.
  print("Oops! That wasn't a valid number. 😟")

except ZeroDivisionError:
  # 3. This block runs ONLY if a ZeroDivisionError occurs.
  print("Oops! You can't divide by zero. 🚫")
```
Python will try to run the code in the `try` block. If an exception occurs, it will look for a matching `except` block and run that code. If no exception occurs, the `except` blocks are skipped.

**Best Practice:** Always try to catch the *most specific* exception possible. Avoid using a bare `except:` or `except Exception:`, as this can hide bugs by catching errors you didn't expect.

### 2. The `else` and `finally` Clauses

These provide even more control over the flow.

*   `else`: This block runs if the `try` block completes **without raising any exceptions**.
*   `finally`: This block runs **no matter what**. It runs if there was an exception, if there wasn't an exception, even if you `return` from inside the `try` block. It's perfect for cleanup.

```python
f = None # Initialize f to None
try:
    f = open("my_file.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("Oh no, the file doesn't exist!")
else:
    # This runs only if the file was opened successfully
    print("File read successfully!")
    print(f"Content: {content}")
finally:
    # This runs whether the file was found or not
    if f: # Check if the file was successfully opened before trying to close it
        f.close()
    print("--- End of operation ---")
```

### 3. Raising Your Own Exceptions

Sometimes, you need to raise an exception yourself to signal that something is wrong based on your program's logic. You do this with the `raise` keyword.

```python
def set_age(age):
  if age < 0:
    # Raise a ValueError with a helpful message
    raise ValueError("Age cannot be negative.")
  if age > 120:
    raise ValueError("Age seems unlikely. Are you a vampire? 🧛")
  print(f"Age set to {age}")

try:
  set_age(-10)
except ValueError as e:
  # 'e' contains the exception object with our message
  print(f"Error: {e}")
```

Proper exception handling is a critical skill for writing professional, production-ready Python code.

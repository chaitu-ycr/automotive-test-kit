# 🎁 015: Decorators

Imagine you have several functions, and for each one, you need to log when it starts and when it finishes. You could add `print()` statements at the beginning and end of every function, but that's repetitive and clutters up your core logic.

What if you could "wrap" your functions in another function that adds this logging behavior automatically? That's exactly what a **decorator** does. A decorator is a special kind of function that takes another function as an argument and extends or modifies its behavior without permanently changing its source code.

## 🗺️ A Mind Map of the Decorator Pattern

A decorator is like a wrapper you put around a function.

```mermaid
graph TD
    A[Your Original Function] --> B(Is passed into...)
    B --> C{Decorator Function}
    C --> D[Creates a new 'wrapper' function]
    subgraph Wrapper Function
        E[1. Code to run *before*]
        F[2. Call the original function]
        G[3. Code to run *after*]
    end
    D --> H(Returns the new wrapper function)

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 🤔 What Is a Decorator?

To understand decorators, you first need to know that in Python, **functions are first-class objects**. This means you can:
*   Assign a function to a variable.
*   Pass a function as an argument to another function.
*   Return a function from another function.

A decorator is a direct application of these concepts. It's a function that takes a function as input, adds some functionality inside a "wrapper" function, and returns the wrapper function.

## ✨ Why Are Decorators So Powerful?

Decorators are a cornerstone of clean, advanced Python programming. They allow you to practice **Separation of Concerns**.

*   **DRY (Don't Repeat Yourself):** Instead of adding the same logging/timing/authentication code to 20 different functions, you write one decorator and apply it to all of them.
*   **Clean Code:** Your core business logic (e.g., `calculate_payment()`) is not cluttered with boilerplate code for logging or caching. It remains focused on its one job.
*   **Reusability:** A single decorator can be used to enhance many different functions across your entire application.
*   **Extensibility:** You can easily add or remove functionality from a function by simply adding or removing a decorator line, without ever touching the function's code.

Common use cases include logging, performance timing, caching results, and checking for user authentication in web frameworks like Flask and Django.

---

## 🚀 How Do I Create and Use Decorators?

Let's build a decorator step-by-step.

### 1. The Basic Structure

A decorator is a function that returns another function.

```python
def my_decorator(original_func):
  # This is the wrapper function that adds the new behavior.
  # It accepts any arguments the original function might take.
  def wrapper(*args, **kwargs):
    # 1. Do something BEFORE the original function is called.
    print(f"Running '{original_func.__name__}'...")

    # 2. Call the original function with its arguments.
    result = original_func(*args, **kwargs)

    # 3. Do something AFTER the original function is called.
    print(f"Finished '{original_func.__name__}'.")

    # 4. Return the result from the original function.
    return result

  # The decorator returns the wrapper function.
  return wrapper
```

### 2. Applying the Decorator with `@`

The `@` symbol is "syntactic sugar" that makes applying decorators clean and readable.

```python
@my_decorator
def say_hello(name):
  print(f"Hello, {name}!")

# Now, when we call say_hello, we are actually calling the wrapper.
say_hello("Alice")
```
This will output:
```
Running 'say_hello'...
Hello, Alice!
Finished 'say_hello'.
```
The line `@my_decorator` is just a shortcut for `say_hello = my_decorator(say_hello)`.

### 3. A Practical Example: A Timing Decorator

Let's create a useful decorator that measures how long a function takes to run.

```python
import time

def timer(func):
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"'{func.__name__}' took {end_time - start_time:.4f} seconds to run.")
    return result
  return wrapper

@timer
def process_data(size):
  """A dummy function that simulates some work."""
  print(f"Processing {size} items...")
  time.sleep(size) # Simulate work by sleeping
  print("Processing complete.")
  return "Done"

process_data(2)
```
This will output something like:
```
Processing 2 items...
Processing complete.
'process_data' took 2.0012 seconds to run.
```

Now you can add `@timer` to any function in your codebase to easily measure its performance! That's the power of decorators.

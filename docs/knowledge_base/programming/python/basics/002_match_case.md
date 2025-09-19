# 🧩 002: Pattern Matching with `match` and `case`

Introduced in Python 3.10, the `match-case` statement is a powerful feature that acts like a supercharged `if-elif-else` chain. It's designed to handle complex conditional logic in a way that is both readable and efficient, especially when you're working with structured data.

## 🗺️ A Mind Map of `match-case` Patterns

This statement is all about matching patterns. Here are some of the most common patterns you can use:

```mermaid
mindmap
  root((match-case Patterns))
     Literals
       `case 42:`
       `case "Hello":`
       `case True:`
     Sequences
       `case [x, y]:` (List of two items)
       `case (x, 0):` (Tuple on the x-axis)
       `case [x, *others]:` (Capture rest of the list)
     Mappings (Dictionaries)
       `case {"name": name, "age": age}:`
     OR Patterns
       `case "PENDING" | "QUEUED":`
     Guards (if conditions)
       `case [x, y] if x == y:`
     Wildcard (Catch-all)
       `case _:`
```

---

## 🤔 What Is a `match-case` Statement?

A `match-case` statement takes an expression and compares it against a series of `case` patterns. As soon as it finds a pattern that matches, it executes the code for that block and then stops.

Think of it as a switchboard operator:
1.  An incoming call (`match expression`) arrives.
2.  The operator checks the first line (`case pattern1`). Is it the right one? No.
3.  They check the second line (`case pattern2`). A match! They connect the call (`execute the code`).
4.  The job is done, and they don't check any other lines.
5.  If no line matches, they send it to a default operator (`case _:`).

## ✨ Why Is This So Powerful?

You might be thinking, "Can't I just use `if-elif-else`?" Yes, you can, but `match-case` offers some fantastic advantages:

*   **Improved Readability:** For complex conditions, `match-case` is often cleaner and easier to read than a long chain of `if-elif` checks. It clearly states, "Here's the data, now find the pattern that fits."
*   **Destructuring on the Fly:** This is its superpower! You can match complex data types (like lists, tuples, and dictionaries) and pull out the values you need, all in one step. No more `if isinstance(...)` followed by accessing elements or keys.
*   **Built for Structured Data:** It shines when you're working with data that has a predictable structure, like API responses, configuration files, or command parsers.

**Important Note:** `match-case` is only available in **Python 3.10 and newer**. For older versions, you'll need to stick with `if-elif-else`.

---

## 🚀 How Do I Use It?

The syntax is straightforward. You start with `match` followed by the value you want to test. Then, you define your `case` patterns.

### Basic Example: Handling Status Codes

Imagine you're processing a task, and it can have different statuses.

```python
status = "COMPLETED"

match status:
    case "PENDING" | "QUEUED":
        print("The task is waiting to be processed. ⏳")
    case "IN_PROGRESS":
        print("The task is currently running. ⚙️")
    case "COMPLETED":
        print("The task finished successfully! ✅")
    case "FAILED":
        print("Something went wrong. ❌")
    case _: # This is the wildcard/default case
        print(f"Unknown status: {status}")

```
This is much cleaner than four separate `if/elif` statements! Notice the `|` (OR) pattern to combine two cases.

### Advanced Example: Destructuring a Point 📍

This is where `match-case` truly shines. Let's say we have a point represented by a tuple `(x, y)` and we want to describe its location.

```python
point = (0, 5)

match point:
    case (0, 0):
        print("The point is at the origin (0, 0).")
    case (0, y):
        print(f"The point is on the Y-axis at y={y}.")
    case (x, 0):
        print(f"The point is on the X-axis at x={x}.")
    case (x, y):
        print(f"The point is at coordinates ({x}, {y}).")
    case _:
        print("This is not a valid 2D point.")
```
In one clean block, we've handled four different structural patterns and extracted the `x` and `y` values without needing to access `point[0]` or `point[1]`.

### Using Guards: Adding an `if` Condition

You can add an `if` condition to a pattern for even more specific matching. This is called a **guard**.

```python
point = (5, 5)

match point:
    case (x, y) if x == y:
        print(f"The point is at coordinates ({x}, {y}) and it lies on the y=x line. ✨")
    case (x, y):
        print(f"The point is at coordinates ({x}, {y}).")
```
The first `case` will only match if `x` and `y` are equal.

---

`match-case` is a fantastic, modern Python feature that can make your code more elegant and robust. Give it a try next time you find yourself writing a long `if-elif-else` chain!

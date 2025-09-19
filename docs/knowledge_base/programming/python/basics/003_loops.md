# 🔁 003: Repeating Actions with Loops

Imagine you had to write `print("Hello")` one hundred times. That would be tedious! In programming, we often need to repeat actions, and doing it manually is out of the question. This is where loops come to the rescue. They are a fundamental concept for automation and iteration.

## 🗺️ A Mind Map of Python Loops

Python provides two main ways to create loops, each with its own specialty. Here’s a quick overview:

```mermaid
mindmap
  root((Python Loops))
    --> For Loops (Iterating over a sequence)
      --> `for item in list:`
      --> `for number in range(5):`
      --> `for index, value in enumerate(list):`
    --> While Loops (Looping as long as a condition is true)
      --> `while count < 10:`
      --> `while not is_finished:`
    --> Loop Control
      --> `break` (Exit the loop entirely)
      --> `continue` (Skip to the next iteration)
      --> `else` (Run if the loop finishes without a `break`)
```

---

## 🤔 What Are Loops?

Loops are control structures that allow you to execute a block of code repeatedly. Instead of writing the same code over and over, you write it once inside a loop.

Python has two primary types of loops:
*   **`for` loops:** Used when you want to iterate over a sequence of items (like a list, a string, or a range of numbers) and perform an action for each item.
*   **`while` loops:** Used when you want to repeat a block of code as long as a certain condition remains true.

## ✨ Why Are Loops So Important?

Loops are the workhorses of programming. They allow you to:

*   **Automate Repetitive Tasks:** Process thousands of files, send a hundred emails, or calculate the total of a million numbers without writing a million lines of code.
*   **Work with Collections of Data:** Easily handle each item in a list, each character in a string, or each row in a dataset.
*   **Create Dynamic Programs:** Build games that run until a player quits, or servers that listen for connections indefinitely.

Without loops, programming would be incredibly inefficient and limited.

---

## 🚀 How Do I Use Them?

Let's dive into how to build `for` and `while` loops.

### 1. The `for` Loop: The Item-by-Item Iterator

Use a `for` loop when you have a collection of items and you want to do something with each one.

**Syntax:** `for item in sequence:`

#### Real-World Example: A Shopping List 🛒

Let's say you want to print out every item on your shopping list.

```python
shopping_list = ["apples 🍎", "bread 🍞", "milk 🥛", "coffee ☕"]

print("My Shopping List:")
for item in shopping_list:
    print(f"- {item}")
```

This loop takes each `item` from the `shopping_list` one by one and executes the `print` statement for it.

#### Looping a Specific Number of Times with `range()`

If you need to repeat an action a certain number of times, `range()` is your best friend.

```python
# range(5) generates numbers from 0 up to (but not including) 5.
print("Counting to 4:")
for number in range(5):
    print(number)
```

### 2. The `while` Loop: The Condition Checker

Use a `while` loop when you want to keep looping as long as a condition is `True`.

**Syntax:** `while condition:`

**⚠️ Warning:** Be careful! If the condition never becomes `False`, you'll create an **infinite loop**, and your program will run forever. Always make sure there's a way for the loop to end.

#### Real-World Example: A Rocket Launch Countdown 🚀

```python
countdown = 10

print("Preparing for launch...")
while countdown > 0:
    print(f"{countdown}...")
    countdown -= 1 # This is crucial! It moves us closer to the end condition.

print("Liftoff! 🚀")
```
This loop continues as long as `countdown` is greater than 0. The `countdown -= 1` line ensures the condition eventually becomes `False`.

### 3. Controlling Your Loops: `break` and `continue`

Sometimes you need more fine-grained control over your loops.

*   `break`: Stops the loop immediately, no matter what.
*   `continue`: Skips the rest of the current iteration and jumps to the next one.

#### Example: Finding the First Admin User

Imagine you're searching through a list of users to find the first admin. Once you find them, you can stop searching.

```python
users = ["guest", "user1", "user2", "admin", "user3"]

for user in users:
    print(f"Checking user: {user}")
    if user == "admin":
        print("Admin found! Stopping the search. ✅")
        break # Exit the loop!
```

#### Example: Printing Only Odd Numbers

Let's use `continue` to skip all the even numbers in a range.

```python
for number in range(10):
    if number % 2 == 0: # If the number is even...
        continue # ...skip to the next iteration.
    print(number) # This line only runs for odd numbers.
```

With `for` and `while` loops, you've unlocked the power of automation in Python!

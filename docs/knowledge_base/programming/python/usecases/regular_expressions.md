# 🧐 Usecase: Pattern Matching with Regular Expressions

Simple string methods like `.find()` are great if you know the exact text you're looking for. But what if you need to find a *pattern*? For example, how would you find all the email addresses in a document, or extract all the phone numbers from a web page?

For this, you need a more powerful tool: **Regular Expressions** (often shortened to "regex"). A regular expression is a special sequence of characters that defines a search pattern. Python's built-in `re` module is the key to unlocking this power.

## 🗺️ A Mind Map of the `re` Module

The `re` module's workflow is simple: you define a pattern and then use a function to apply that pattern to your text.

```mermaid
mindmap
  root((Regular Expressions))
    --> The Pattern (Your Search Query)
      --> Literals: `a`, `cat`
      --> Character Sets: `\d` (digit), `\w` (word char), `\s` (space)
      --> Quantifiers: `+` (1+), `*` (0+), `?` (0 or 1)
      --> Anchors: `^` (start), `$` (end)
      --> Groups: `(...)`
    --> The Functions (The Actions)
      --> `re.findall()`: Find ALL matching substrings
      --> `re.search()`: Find the FIRST match anywhere
      --> `re.sub()`: Find and REPLACE
      --> `re.split()`: Split the string by the pattern
```

---

## 🤔 What Are Regular Expressions?

A regular expression is a mini-language for identifying patterns in text. Instead of searching for a literal string like `"apple"`, you can search for a pattern like `r"\d+"`, which means "one or more digits." This would find `"12"`, `"456"`, or any sequence of numbers.

## ✨ Why Are Regular Expressions So Useful?

*   **Powerful Validation:** They are perfect for checking if user input matches a required format, like an email address, a phone number, or a password with specific rules.
*   **Advanced Find and Replace:** You can perform complex substitutions that would be impossible with simple `.replace()`, like swapping the first and last names in a list.
*   **Data Extraction (Scraping):** They are essential for pulling structured data (like product prices or dates) out of unstructured text like log files or HTML.
*   **Flexibility:** The pattern-matching language is incredibly expressive, allowing you to define almost any rule you can imagine.

---

## 🚀 How Do I Use the `re` Module?

Let's explore the most common functions in the `re` module.

### 1. `re.findall()` - Find All Matches

This is often the most useful function. It scans a string from left to right and returns a list of all non-overlapping matches of your pattern.

```python
import re

text = "My phone number is 415-555-1234, but you can also reach me at (415) 555-9876."

# The pattern r"\d{3}-\d{3}-\d{4}" means:
# \d{3} - exactly 3 digits
# -     - a literal hyphen
# \d{4} - exactly 4 digits
phone_numbers = re.findall(r"\d{3}-\d{3}-\d{4}", text)

print(phone_numbers)
# Output: ['415-555-1234']
```
Notice it didn't find the second number because the pattern was too specific. Let's make it more flexible.

### 2. Capturing Groups `()`

Parentheses `()` in a pattern create a "capturing group." This tells `findall` to return only the part of the match inside the parentheses. It's also great for creating more complex patterns.

```python
# Let's create a more flexible pattern
# \(? - an optional opening parenthesis
# \d{3} - 3 digits
# \)? - an optional closing parenthesis
# [-\s]? - an optional hyphen or space
pattern = r"\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{4})"

# findall with groups returns a list of tuples, where each tuple contains the captured groups
matches = re.findall(pattern, text)
print(matches)
# Output: [('415', '555', '1234'), ('415', '555', '9876')]
```

### 3. `re.search()` - Find the First Match

`search()` scans the string and returns a **match object** for the *first* location where the pattern produces a match. If no match is found, it returns `None`.

```python
text = "The quick brown fox jumps over the lazy dog."

match = re.search(r"fox", text)

if match:
  print("Match found!")
  print(f"Start index: {match.start()}")
  print(f"End index: {match.end()}")
  print(f"Matched string: {match.group(0)}")
else:
  print("No match found.")
```

### 4. `re.sub()` - Find and Replace

`sub()` replaces all occurrences of a pattern with a specified string.

```python
text = "Hello, my name is Alice. Hello, Bob."

# Replace all occurrences of "Hello" with "Hi"
new_text = re.sub(r"Hello", "Hi", text)

print(new_text)
# Output: Hi, my name is Alice. Hi, Bob.
```

### 5. Compiling Patterns with `re.compile()`

If you're going to use the same pattern multiple times, it's more efficient to compile it first. This creates a pattern object that you can reuse.

```python
text = "John: 30, Jane: 25, David: 40"

# Compile a pattern to find names
name_pattern = re.compile(r"[A-Z][a-z]+")

names = name_pattern.findall(text)
print(names)
# Output: ['John', 'Jane', 'David']
```
Regular expressions are a deep and powerful topic, but mastering these few functions will allow you to solve a huge range of text processing problems.

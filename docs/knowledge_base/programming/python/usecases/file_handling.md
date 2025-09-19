# 📁 Usecase: Reading and Writing Files

Programs need a way to save data permanently so it can be used later. Whether you're saving user preferences, logging application errors, or processing a large dataset, you need to interact with files. **File handling** (also known as File I/O) is the way your Python program reads from and writes to files on your computer.

## 🗺️ A Mind Map of File Handling

The core of file handling is the `open()` function, which gives you a "file object" to work with. The `with` statement is the safest way to use it.

```mermaid
mindmap
  root((File Handling))
    --> The `open()` function
      --> Takes `filename` and `mode`
    --> The `with` Statement (Best Practice)
      --> `with open(...) as f:`
      --> **Automatically closes the file!** ✅
    --> File Modes
      --> `'r'` (Read): Default mode. Error if file doesn't exist.
      --> `'w'` (Write): Overwrites file! Creates it if it doesn't exist.
      --> `'a'` (Append): Adds to the end. Creates it if it doesn't exist.
      --> `'+'` (Update): `r+`, `w+`, `a+` for reading and writing.
      --> `'b'` (Binary): For non-text files like images or executables.
    --> Common Operations
      --> `f.read()`: Read the whole file.
      --> `f.readline()`: Read one line.
      --> `f.readlines()`: Read all lines into a list.
      --> `f.write()`: Write a string to the file.
```

---

## 🤔 What Is File Handling?

File handling is the process of using your program to create, open, read, write, and delete files. The central function is `open(file_path, mode)`, which returns a file object that you can use to perform these operations.

## ✨ Why Is the `with` Statement So Important?

When you open a file, you are using a system resource. It's crucial that you **close the file** when you're done with it to release that resource and ensure that all data is written correctly.

You could do this manually with `f.close()`, but what if an error happens before you get to that line? The file might be left open.

The `with` statement (also known as a context manager) solves this problem elegantly.
```python
with open("my_file.txt", "w") as f:
  f.write("Hello, World!")
# The file is automatically and safely closed here,
# even if an error occurred inside the 'with' block.
```
**Best Practice:** Always use the `with open(...) as ...:` syntax. It's safer, cleaner, and the universally accepted way to handle files in Python.

---

## 🚀 How Do I Work with Files?

Let's look at the most common file operations.

### 1. Writing to a File (`'w'` mode)

The `'w'` mode is for writing. **Be careful:** it will completely overwrite any existing content in the file. If the file doesn't exist, it will be created.

```python
# This will create 'greetings.txt' and write a single line to it.
with open("greetings.txt", "w") as f:
  f.write("Hello from Python! 👋\n")
  f.write("This is the second line.")
```

### 2. Appending to a File (`'a'` mode)

The `'a'` mode is for appending. It adds new content to the *end* of the file without deleting what's already there. If the file doesn't exist, it will be created.

```python
# Add another line to our existing file.
with open("greetings.txt", "a") as f:
  f.write("\nThis line was appended later.")
```

### 3. Reading a File (`'r'` mode)

The `'r'` mode is for reading. This is the default mode if you don't specify one.

**Reading the whole file at once:**
Good for small files.
```python
with open("greetings.txt", "r") as f:
  content = f.read()
  print("--- Full Content ---")
  print(content)
```

**Reading line by line:**
This is the most memory-efficient way to read large files, as it only loads one line into memory at a time.
```python
with open("greetings.txt", "r") as f:
  print("\n--- Line by Line ---")
  for line in f:
    # .strip() removes leading/trailing whitespace, including the newline character
    print(line.strip())
```

### 4. Working with the `os` Module

For operations on the file itself (like checking for existence or deleting), you need the `os` module.

```python
import os

filename = "greetings.txt"

# Check if a file exists
if os.path.exists(filename):
  print(f"\n'{filename}' exists! ✅")
else:
  print(f"'{filename}' does not exist. ❌")

# Delete a file
# os.remove(filename)
# print(f"'{filename}' has been deleted.")
```

File handling is a fundamental skill that opens the door to data persistence, logging, and interacting with the wider operating system.

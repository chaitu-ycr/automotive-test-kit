# 🗝️ 008: Storing Labeled Data with Dictionaries

Lists are great for ordered sequences, but what if you want to store data with labels? Imagine a phone book where you look up a person's name to get their number. You don't care about the order; you care about the connection between the name (the **key**) and the number (the **value**). This is exactly what a **dictionary** is for.

Dictionaries are Python's implementation of a data structure that stores **key-value pairs**. They are incredibly flexible and are one of the most important data types you'll use.

## 🗺️ A Mind Map of Dictionary Features

Dictionaries are all about the relationship between a unique key and its associated value.

```mermaid
mindmap
  root((Dictionaries))
    --> Structure
      --> `my_dict = {"key": "value"}`
      --> Keys must be **unique** and **immutable**
      --> Values can be anything
    --> Creating & Accessing
      --> `person = {"name": "Alice", "age": 30}`
      --> Access value: `person["age"]`
      --> Safe access: `person.get("email", "N/A")`
    --> Modifying
      --> Add/Update: `person["city"] = "New York"`
      --> Remove: `del person["age"]`, `.pop("age")`
    --> Iterating
      --> Over keys: `for key in my_dict:`
      --> Over values: `for value in my_dict.values():`
      --> Over both: `for key, value in my_dict.items():`
```

---

## 🤔 What Is a Dictionary?

A dictionary is a **mutable** collection that stores data in key-value pairs. It's **unordered** in older Python versions, but as of **Python 3.7+, dictionaries remember the order of insertion**.

*   **Key:** A unique identifier for a value. Must be an immutable type (like a string, number, or tuple).
*   **Value:** The data associated with a key. Can be of any data type (a string, a list, even another dictionary).

You create a dictionary using curly braces `{}` with `key: value` pairs.

```python
# A dictionary representing a user profile
user_profile = {
    "username": "py_master",
    "email": "master@python.org",
    "level": "Expert",
    "favorite_tools": ["VS Code", "Pytest", "Jupyter"]
}
```

## ✨ Why Are Dictionaries So Important?

Dictionaries are the backbone of structured data management in Python.

*   **Fast Lookups:** Retrieving a value by its key is extremely fast, no matter how large the dictionary is. This is much more efficient than searching for an item in a long list.
*   **Meaningful Data:** Keys give your data context. `person["age"]` is much more readable and less error-prone than `person[1]`.
*   **Flexibility:** They are perfect for representing real-world objects and complex data structures, like JSON from a web API.

You'll use dictionaries everywhere, from web development to data science to automation scripts.

---

## 🚀 How Do I Work with Dictionaries?

Let's explore how to create, access, and modify dictionary data.

### 1. Accessing, Adding, and Updating

You use square brackets `[]` with the key to access or modify values.

```python
# Accessing a value by its key
print(f"Username: {user_profile['username']}")

# Adding a new key-value pair
user_profile["country"] = "USA"
print(f"Country added: {user_profile['country']}")

# Updating an existing value
user_profile["level"] = "God Tier"
print(f"New level: {user_profile['level']}")
```

**Safe Access with `.get()`**
If you try to access a key that doesn't exist using `[]`, your program will crash with a `KeyError`. The `.get()` method is a safer way to access values, as it returns `None` (or a default value you provide) if the key is not found.

```python
# This would cause an error: user_profile["phone"]
# The safe way:
phone_number = user_profile.get("phone", "No phone number provided.")
print(phone_number)
```

### 2. Removing Items

You can remove items using `del` or the `.pop()` method.

```python
# Remove a key-value pair using del
del user_profile["email"]

# Remove a key and get its value back using .pop()
tools = user_profile.pop("favorite_tools")
print(f"Removed tools: {tools}")
```

### 3. Looping Through a Dictionary

There are several ways to iterate through a dictionary. The most common is using the `.items()` method to get both the key and value at the same time.

```python
print("\nUser Profile:")
for key, value in user_profile.items():
    print(f"- {key.title()}: {value}")
```

You can also loop through just the keys or just the values:

```python
# Loop through keys (this is the default behavior)
for key in user_profile:
    print(f"Key: {key}")

# Loop through values
for value in user_profile.values():
    print(f"Value: {value}")
```

Dictionaries provide a powerful and intuitive way to structure your data. Mastering them is a key step to becoming a proficient Python programmer!

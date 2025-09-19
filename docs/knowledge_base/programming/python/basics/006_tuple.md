# 🍇 006: Storing Unchanging Data with Tuples

Meet the tuple, the close cousin of the list. Tuples, like lists, are used to store a collection of items in a specific order. However, they have one crucial difference: they are **immutable**. Once you create a tuple, you cannot change it. This makes them perfect for data that you want to protect from accidental modification.

## 🗺️ A Mind Map of Tuple Characteristics

Here's a quick look at what makes tuples unique and useful.

```mermaid
mindmap
  root((Tuples))
    --> Key Properties
      --> **Immutable** (Cannot be changed!)
      --> Ordered (Items have a defined sequence)
      --> Can be used as dictionary keys
    --> Creating & Accessing
      --> `my_tuple = (1, "a", True)`
      --> Special case: `single_item = (42,)`
      --> Indexing: `my_tuple[0]`
      --> Slicing: `my_tuple[1:3]`
    --> Superpower
      --> Tuple Unpacking: `x, y, z = my_tuple`
    --> Common Uses
      --> Returning multiple values from functions
      --> Storing fixed data (e.g., coordinates, RGB colors)
      --> Configuration settings
```

---

## 🤔 What Is a Tuple?

A tuple is an **ordered and immutable** collection of items. You create a tuple by placing items inside parentheses `()`, separated by commas.

```python
# A tuple of RGB color values
red_color = (255, 0, 0)

# A tuple can hold mixed data types
person_data = ("Alice", 30, "Engineer")

# The parentheses are sometimes optional, but it's good practice to use them
coordinates = 10, 20 # This also creates a tuple!
```

**⚠️ Special Case:** To create a tuple with only one item, you **must** include a trailing comma. Without it, Python just sees the value inside the parentheses.

```python
not_a_tuple = (42)   # This is just the integer 42
is_a_tuple = (42,) # The comma makes it a tuple
```

## ✨ Why Are Tuples So Important?

If lists can do everything tuples can do and more, why do we need tuples? Their immutability is not a limitation; it's a feature!

*   **Data Integrity:** When you store data in a tuple, you can be sure that it won't be accidentally changed elsewhere in your program. This is great for constants or configuration settings.
*   **Dictionary Keys:** Lists cannot be used as keys in a dictionary because they are mutable. Tuples, being immutable, can! This is useful for complex keys, like geographic coordinates.
*   **Performance:** Tuples are slightly more memory-efficient and faster to process than lists, making them a good choice for large collections of constant data.
*   **Returning Multiple Values:** It's a common Python convention to use a tuple to return multiple values from a function, which can then be easily unpacked.

---

## 🚀 How Do I Work with Tuples?

Working with tuples is very similar to working with lists, except you can't modify them.

### 1. Accessing and Slicing

This works exactly like lists. You use the index to get an item or a slice to get a sub-tuple.

```python
#           0      1         2
weekdays = ("Mon", "Tue", "Wed", "Thu", "Fri")

# Get the first day
first_day = weekdays[0] # "Mon"

# Get a slice
mid_week = weekdays[1:4] # ("Tue", "Wed", "Thu")

print(f"The first day is: {first_day}")
print(f"The middle of the week is: {mid_week}")
```

### 2. The Superpower: Tuple Unpacking ✨

Tuple unpacking is an elegant and highly "Pythonic" way to assign the elements of a tuple to multiple variables at once.

```python
point = (100, 200)

# The Pythonic way to unpack
x, y = point

print(f"The x-coordinate is {x}") # 100
print(f"The y-coordinate is {y}") # 200
```
This is incredibly useful for swapping variables or handling functions that return multiple values.

```python
# Classic variable swap
a = 5
b = 10
a, b = b, a # Unpacking a tuple `(10, 5)` on the fly!
print(f"a is now {a}, and b is now {b}")
```

### 3. Looping Through a Tuple

You can loop through a tuple just like you would with a list.

```python
for day in weekdays:
    print(f"Today is {day}")
```

### 4. What You CAN'T Do

Remember, tuples are immutable. The following operations will result in an error:

```python
# weekdays[0] = "Sunday"      # ❌ TypeError
# weekdays.append("Sat")      # ❌ AttributeError: 'tuple' object has no attribute 'append'
# del weekdays[0]             # ❌ TypeError
```
If you need to modify the data, you should use a list instead. Or, you can create a *new* tuple based on the old one.

```python
# Create a new tuple by concatenating
weekend = ("Sat", "Sun")
full_week = weekdays + weekend
print(full_week)
```

Tuples are a simple but powerful tool for writing safe, readable, and efficient Python code.

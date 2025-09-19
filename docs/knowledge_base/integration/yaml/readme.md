# 📝 YAML: The Human-Friendly Config Language

Welcome to YAML (a recursive acronym for "YAML Ain't Markup Language")! If you've ever worked with configuration files, CI/CD pipelines, or Docker, you've probably met YAML. It's a data serialization language designed to be incredibly easy for humans to read and write.

This guide will walk you through the core syntax and features of YAML, from simple key-value pairs to more advanced structures, all with practical examples.

> **Note:**  
> - 🧑‍💻 YAML uses spaces (not tabs) for indentation.  
> - 📏 Indentation defines structure and hierarchy.

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [YAML at a Glance (Mindmap)](#yaml-at-a-glance-mindmap)
3. [Syntax Basics](#syntax-basics)
4. [Scalars](#scalars)
5. [Collections](#collections)
6. [Advanced Features](#advanced-features)
7. [Miscellaneous](#miscellaneous)
8. [YAML in Python](#yaml-in-python)
9. [Quick Reference](#quick-reference)

---

## 2. 🗺️ YAML at a Glance (Mindmap)

```mermaid
mindmap
  root((YAML))
    Core Concepts
      Syntax
        Indentation (Spaces only!)
        Key-Value Pairs (`key: value`)
        Comments (`#`)
      Data Types
        Scalars (Single Values)
          Strings (quoted or unquoted)
          Numbers (`123`, `3.14`)
          Booleans (`true`, `false`)
          Null (`null` or `~`)
        Collections (Groups of Data)
          Sequences (Lists)
            `- item1`
            `- item2`
          Mappings (Dictionaries)
            `key1: value1`
            `key2: value2`
    Advanced Features
      Anchors (`&`) & Aliases (`*`)
      Multi-line Strings (`|` or `>`)
      Multi-Document (`---`)
```

---

## 🚀 Tutorial: Building a `config.yml` File

The best way to learn YAML is to build something real. Let's create a typical configuration file (`config.yml`) for a hypothetical web application.

### Step 1: Basic Key-Value Pairs

Every application needs some basic settings. Let's define the application's name and the port it should run on. This is a simple `key: value` structure.

```yml
# The name of our application
app_name: "My Awesome Web App"

# The port the server will listen on
port: 8080
```

### Step 2: Adding Nested Data (Mappings)

Configurations often have grouped settings, like for a database connection. We can create a nested "object" or "mapping" by indenting key-value pairs under a parent key.

```yml
app_name: "My Awesome Web App"
port: 8080

# Database connection settings
database:
  host: "localhost"
  port: 5432
  user: "db_user"
  password: "secure_password" # In a real app, use secrets management!
```

### Step 3: Using Booleans and Nulls

Let's add a feature flag to enable or disable debugging, and a setting for a feature that isn't configured yet.

```yml
app_name: "My Awesome Web App"
port: 8080

database:
  host: "localhost"
  port: 5432
  user: "db_user"
  password: "secure_password"

# Enable debug mode for development
debug_mode: true

# API key for a service we haven't set up yet
external_api_key: null
```

### Step 4: Adding Lists of Items (Sequences)

Finally, let's define a list of admin users who have special privileges in the application. A list in YAML is a sequence of items, each starting with a hyphen (`-`).

```yml
app_name: "My Awesome Web App"
port: 8080

database:
  host: "localhost"
  port: 5432
  user: "db_user"
  password: "secure_password"

debug_mode: true
external_api_key: null

# A list of admin users
admin_users:
  - "alice"
  - "bob"
  - "charlie"
```

### Final `config.yml`

Congratulations! You've created a complete, easy-to-read configuration file that uses YAML's most common features: key-value pairs, nested objects, booleans, nulls, and lists.

This file is now ready to be loaded by your application to configure its settings.

---

## 1. 🏁 Introduction

YAML is a popular, human-friendly data format for configuration files and data exchange.  
**Key features:**  
- Indentation-based structure (no braces or brackets)
- Supports complex data types (lists, dictionaries, etc.)
- Widely used in DevOps, CI/CD, and programming

---

## 2. 🔤 Syntax Basics

The two most important rules in YAML are about how you structure the file: **indentation** and **comments**. Getting these right is the key to a valid YAML file.

### Indentation & Whitespace

- **Spaces Only:** No tabs allowed.
- **Consistent Indent:** Indentation defines structure.

```yml
key1: value1
key2:
  nestedKey1: nestedValue1
  nestedKey2: nestedValue2
```

**❌ Incorrect (tabs cause errors):**
```yml
key1:
<TAB>nestedKey: value
```

### Comments

- Single-line: `# This is a comment`
- Inline: `name: automotive-test-kit  # Inline comment`

```yml
# This is a comment
name: automotive-test-kit  # Inline comment
```

---

## 3. 🔢 Scalars

How do you represent a single piece of data, like a name, a number, or a simple 'yes'/'no' value? In YAML, these are called **scalars**. Let's look at the different ways you can write them.

### String Styles

| Style         | Example                        | Notes                        |
|---------------|-------------------------------|------------------------------|
| Plain         | `name: automotive-test-kit`            | Unquoted                     |
| Single Quotes | `text: 'It''s a sunny day'`   | Escape `'` as `''`           |
| Double Quotes | `text: "Hello, \nWorld!"`     | Supports escapes             |
| Emoji         | `emoji: "😀😃😄"`              | Unicode supported            |

#### Multiline Strings

| Style         | Syntax Example         | Preserves Line Breaks? | Description                  |
|---------------|-----------------------|------------------------|------------------------------|
| Block (`|`)   | `block_scalar: | ...` | ✅ Yes                 | Keeps line breaks            |
| Folded (`>`)  | `folded_scalar: > ...`| ❌ No (folds to spaces)| Folds newlines into spaces   |

```yml
block_scalar: |
  This is a block scalar.
  It preserves line breaks.

folded_scalar: >
  This is a folded scalar.
  It folds new lines into spaces,
  creating a single flowing paragraph.
```

#### Special Characters

- Double quotes allow escapes:  
  `special: "Newline: \n, Tab: \t, Quote: \""`

---

### Numbers & Type Tags

| Type         | Example                        | Description                        |
|--------------|-------------------------------|------------------------------------|
| Integer      | `age: 30`                     | Whole number 🔢                    |
| Negative     | `temperature: -5`             | Negative integer ❄️                |
| Float        | `height: 5.9`                 | Decimal number 💧                  |
| Scientific   | `speed: 3.0e8`                | Exponential notation 🚀            |
| Hexadecimal  | `color: 0xFF5733`             | Hex number 🎨                      |
| Octal        | `perm: 0755`                  | File permissions 🗂️                |
| Binary       | `bin: 0b101010`               | Binary number 💾                   |
| Explicit Tag | `!!int "42"`, `!!float "3.14"`| Explicit type tags 🏷️              |

---

### Booleans

| True Values         | False Values        |
|---------------------|--------------------|
| `true` ✅, `yes` 👍, `on` 🔛 | `false` ❌, `no` 👎, `off` 🔇 |

```yml
is_active: true
has_license: false
is_enabled: yes
is_disabled: no
light_switch: on
dark_mode: off
```

---

### Null

| Representation         | Example                        |
|-----------------------|--------------------------------|
| Explicit `null`       | `preferred_language: null`     |
| Tilde (`~`)           | `shipping_address: ~`          |
| Empty Value           | `phone_number:`                |
| Empty Quotes          | `additional_info: ''`          |

---

## 4. 📦 Collections

How do you represent more complex data, like a list of users or a user's profile? YAML has two powerful tools for this: **Sequences** (which are like lists or arrays) and **Mappings** (which are like dictionaries or hash maps).

### Sequences (Lists)

```yml
fruits:
  - 🍏 Apple
  - 🍌 Banana
  - 🍒 Cherry

mixed_list:
  - "String"
  - 42
  - true
  - null
```

- **Nested lists, lists of dictionaries, and empty lists (`[]`) are supported.**

### Mappings (Dictionaries)

```yml
person:
  name: automotive-test-kit
  age: 30

address: {street: 123 Main St, city: chennai, zip: 12345}
empty_mapping: {}
```

- **Nested mappings, inline mappings, and empty mappings (`{}`) are supported.**

---

## 5. 🛠️ Advanced Features

### Anchors & Aliases

```yml
defaults: &defaults
  country: 🇮🇳 INDIA
  currency: 💸 RUPEE

location1:
  <<: *defaults
  city: chennai
```

### Complex Keys

```yml
? [first, second]
: "Tuple as a key"
```

### Multi-Document Files

```yml
---
document1:
  key1: value1
---
document2:
  key2: value2
...
```

---

## 6. 🧩 Miscellaneous

### Date and Time

```yml
birth_date: 1990-12-31
meeting_time: 14:30:00
event_timestamp: 2023-04-06T14:30:00Z
local_timestamp: 2023-04-06T14:30:00+05:30
date_range: "2023-04-01 to 2023-04-07"
time_range: "14:30:00 to 15:30:00"
```

### Custom Data Types

```yml
!color
name: Blue
code: "#0000FF"
```

---

## 7. 🐍 YAML in Python

### Install PyYAML

```sh
pip install pyyaml
```

### Read YAML

```python
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

data = read_yaml('example.yaml')
print(data)
```

### Write YAML

```python
import yaml

data = {
    'name': 'automotive-test-kit',
    'age': 30,
    'address': {
        'street': '123 Main St',
        'city': 'chennai',
        'zip': 12345
    },
    'hobbies': ['Reading', 'Hiking', 'Coding']
}

def write_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

write_yaml('output.yaml', data)
```

**Sample Output (`output.yaml`):**
```yml
name: automotive-test-kit
age: 30
address:
  street: 123 Main St
  city: chennai
  zip: 12345
hobbies:
- Reading
- Hiking
- Coding
```

---

## 8. 🗂️ Quick Reference

- **Indentation:** Use spaces, not tabs.
- **Comments:** Start with `#`.
- **Strings:** Plain, single-quoted, double-quoted, multiline (`|` or `>`).
- **Numbers:** Integer, float, hex, octal, binary.
- **Booleans:** `true`/`false`, `yes`/`no`, `on`/`off`.
- **Null:** `null`, `~`, empty value, `''`.
- **Lists:** Use `-` for each item.
- **Dictionaries:** `key: value` pairs.
- **Anchors/Aliases:** `&anchor`, `*alias`.
- **Multi-document:** Separate with `---`.
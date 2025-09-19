# ✨ Usecase: Building Modern GUIs with `customtkinter`

Python's built-in library for creating desktop applications, `tkinter`, is powerful and reliable, but let's be honest—it can look a bit dated right out of the box. What if you want to create a simple GUI that looks modern and professional without learning a massive new framework like Qt or wxPython?

This is where `customtkinter` shines. It's a library that builds on top of `tkinter`, giving you beautifully styled, modern, and themeable widgets with a very similar and easy-to-learn API.

## 🗺️ A Mind Map of `customtkinter` Widgets

`customtkinter` provides a suite of modern widgets to build your application's interface.

```mermaid
mindmap
  root((customtkinter App))
    --> The Main Window (`ctk.CTk`)
    --> Layout
      --> Frames (`CTkFrame`)
      --> `.pack()`, `.grid()`, `.place()`
    --> Basic Widgets
      --> Button (`CTkButton`)
      --> Label (`CTkLabel`)
      --> Entry (`CTkEntry`)
    --> Interactive Widgets
      --> Slider (`CTkSlider`)
      --> Switch (`CTkSwitch`)
      --> ComboBox (`CTkComboBox`)
      --> OptionMenu (`CTkOptionMenu`)
    --> Display Widgets
      --> Progress Bar (`CTkProgressBar`)
      --> Text Box (`CTkTextbox`)
```

---

## 🤔 What Is `customtkinter`?

`customtkinter` is a Python UI library that provides modern and fully customizable widgets for `tkinter`. It allows you to create applications that look good on all platforms (Windows, macOS, Linux) and supports light/dark mode theming right out of the box.

## ✨ Why Is `customtkinter` So Useful?

*   **Modern Appearance:** It's the easiest way to make your `tkinter` apps look good. The default themes are sleek and professional.
*   **Simple API:** If you already know a little `tkinter`, you'll feel right at home. The widget names and methods are very similar (e.g., `tkinter.Button` vs `customtkinter.CTkButton`).
*   **Lightweight:** It's a simple drop-in replacement for `tkinter` widgets without adding a huge, complex dependency to your project.
*   **Theming:** Easily switch between light mode, dark mode, or have the app follow the system theme.

It's the perfect choice for small to medium-sized desktop tools, utilities, and hobby projects where you want a nice UI without a steep learning curve.

---

## 🚀 How Do I Build an App with `customtkinter`?

Let's build a simple "Tip Calculator" application to see how the different widgets work together.

### 1. Installation

First, you need to install the library.
```bash
pip install customtkinter
```

### 2. Setting up the Main Window

Every app starts with a main window. In `customtkinter`, this is a `CTk` object.

```python
import customtkinter as ctk

# Set the appearance mode ("System", "Dark", "Light")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("My Awesome App")
app.geometry("400x500") # Width x Height
```

### 3. Adding Widgets and Handling Events

Now, let's add the components for our tip calculator: an entry for the bill, a slider for the tip percentage, and a button to calculate.

```python
# --- Widgets ---

# Title Label
title_label = ctk.CTkLabel(app, text="Tip Calculator", font=ctk.CTkFont(size=20, weight="bold"))
title_label.pack(padx=10, pady=(40, 20)) # Add padding

# Bill Amount Entry
bill_entry = ctk.CTkEntry(app, placeholder_text="Enter bill amount")
bill_entry.pack(padx=10, pady=10)

# Tip Percentage Slider
tip_slider = ctk.CTkSlider(app, from_=0, to=30)
tip_slider.pack(padx=10, pady=10)
tip_slider.set(15) # Default value

# --- Logic ---

def calculate_tip():
  try:
    bill_amount = float(bill_entry.get())
    tip_percentage = tip_slider.get()
    tip_amount = bill_amount * (tip_percentage / 100)
    total_amount = bill_amount + tip_amount
    result_label.configure(text=f"Tip: ${tip_amount:.2f}\nTotal: ${total_amount:.2f}")
  except ValueError:
    result_label.configure(text="Please enter a valid number!")

# --- More Widgets ---

# Calculate Button
calculate_button = ctk.CTkButton(app, text="Calculate", command=calculate_tip)
calculate_button.pack(padx=10, pady=20)

# Result Label
result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=16))
result_label.pack(padx=10, pady=10)

```

### 4. Running the App

Finally, you need to start the application's main event loop. This loop listens for user actions (like button clicks) and keeps the window open.

```python
# This line must be at the end of your script
app.mainloop()
```
When you run this complete script, you'll have a functional and modern-looking tip calculator! It demonstrates how to create widgets, link a function to a button's `command`, and update the UI based on user input.

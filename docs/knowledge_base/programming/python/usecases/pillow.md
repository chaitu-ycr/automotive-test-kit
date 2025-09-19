# 🖼️ Usecase: Image Manipulation with `Pillow`

While libraries like OpenCV are built for complex computer vision analysis, sometimes you just need to perform simple image manipulations: resize a user's profile picture, add a watermark to a photo, or convert a batch of JPEGs to PNGs. For these tasks, **Pillow** is the perfect tool.

Pillow (a friendly fork of the original Python Imaging Library, or PIL) is the de-facto standard library for general-purpose image manipulation in Python. It's user-friendly, powerful, and much simpler to get started with than a heavy-duty computer vision library.

## 🗺️ A Mind Map of Pillow's Functionality

Pillow's power revolves around the `Image` object and the many modules that can operate on it.

```mermaid
mindmap
  root((Pillow))
    --> The `Image` Module (Core)
      --> Open: `Image.open()`
      --> Create New: `Image.new()`
      --> Save: `img.save()`
    --> Image Transformations
      --> `.resize()`
      --> `.crop()`
      --> `.rotate()`
      --> `.transpose()` (Flip)
      --> `.convert()` (e.g., to 'L' for grayscale)
    --> The `ImageDraw` Module
      --> Drawing on an image
      --> `draw.text()`
      --> `draw.line()`, `draw.rectangle()`
    --> The `ImageFilter` Module
      --> Applying filters
      --> `img.filter(ImageFilter.BLUR)`
      --> `img.filter(ImageFilter.CONTOUR)`
```

---

## 🤔 What Is Pillow?

Pillow is a Python library that adds support for opening, manipulating, and saving many different image file formats. The core of the library is the `Image` object, which represents a single image and provides methods for transformations.

## ✨ Why Is Pillow So Useful?

*   **User-Friendly API:** Pillow's methods are intuitive and easy to learn (e.g., `img.resize()`, `img.rotate()`). It feels very "Pythonic."
*   **Wide Format Support:** It can read and write a huge variety of image formats, including JPEG, PNG, BMP, GIF, and TIFF.
*   **Great for Web Development:** It's the standard choice for backend web development tasks like processing user-uploaded images, creating thumbnails, or generating images dynamically.
*   **Lightweight:** It's focused purely on image manipulation, so it's less complex and has fewer dependencies than a full computer vision library.

---

## 🚀 How Do I Use Pillow?

Let's walk through a common workflow: opening an image, applying several edits, and saving the result.

### 1. Installation

First, you need to install the library.
```bash
pip install Pillow
```

### 2. Opening and Inspecting an Image

The first step is always to open an image file, which returns an `Image` object.

```python
from PIL import Image

# Open an image file
try:
    img = Image.open("./_data/opencv/butterfly.jpg")

    # Get some basic information about the image
    print(f"Format: {img.format}")
    print(f"Size: {img.size}") # (width, height)
    print(f"Mode: {img.mode}") # e.g., 'RGB' for color, 'L' for grayscale

    # Show the image (this will open it in your default image viewer)
    img.show()

except FileNotFoundError:
    print("Error: The image file was not found.")
```

### 3. Transforming the Image

Pillow's power lies in its transformation methods. Let's create a thumbnail. Most transformation methods return a *new* `Image` object, leaving the original unchanged.

```python
# Resize the image to create a thumbnail
# The resize method takes a tuple (width, height)
thumbnail = img.resize((200, 150))
thumbnail.show()

# Crop a region of interest from the original image
# The crop method takes a tuple (left, upper, right, lower)
box = (100, 50, 400, 300) # A 300x250 box
cropped_region = img.crop(box)
cropped_region.show()

# Convert the image to grayscale
grayscale_img = img.convert("L")
grayscale_img.show()
```

### 4. Drawing on an Image

To draw text or shapes, you need to use the `ImageDraw` module.

```python
from PIL import ImageDraw, ImageFont

# Make a copy to draw on so we don't alter the original
img_with_text = img.copy()

# Create a drawing context
draw = ImageDraw.Draw(img_with_text)

# You can try to load a specific font, or use the default
try:
    font = ImageFont.truetype("arial.ttf", size=20)
except IOError:
    font = ImageFont.load_default()

# Draw text onto the image
draw.text(
    (10, 10), # (x, y) position for the top-left corner of the text
    "© My Awesome Website",
    font=font,
    fill=(255, 255, 255, 128) # RGBA color for the text
)

img_with_text.show()
```

### 5. Saving the Result

Finally, you can save your new image to a file. Pillow automatically determines the format from the file extension.

```python
# Save the watermarked image as a PNG to preserve transparency
img_with_text.save("butterfly_watermarked.png")

# Save the thumbnail as a high-quality JPEG
thumbnail.save("butterfly_thumbnail.jpg", "jpeg", quality=90)
```
Pillow is an essential tool for any Python developer who needs to work with images in a simple and programmatic way.

# py_clocks

The `py_clocks` package is a Python-based project designed for displaying multiple timezone clocks on a Windows desktop.

By default, the app shows the time in the following timezones:
  - **Asia/Tokyo**
  - **Asia/Kolkata**
  - **Europe/Berlin**

![py_clocks_app](https://chaitu-ycr.github.io/automotive-test-kit/packages/images/py_clocks_app.png)

*Screenshot of the `py_clocks` application showing multiple timezone clocks.*

## Building and Running the Project

```.venv/Scripts/python.exe packages/py_clocks/src/py_clocks/py_clocks.py```

## Creating an Executable

To create a standalone executable for the `py_clocks` package using PyInstaller, use the provided script:

```pyinstaller --onefile packages/py_clocks/src/py_clocks/py_clocks.py```

**Locate the executable**: The generated executable will be located in the `dist` directory as `py_clocks.exe`.

## [source manual](https://chaitu-ycr.github.io/automotive-test-kit/packages/py_clocks/#source-manual)

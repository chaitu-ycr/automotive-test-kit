# pybind11: What, Why, and How

## What is pybind11?

**pybind11** is a lightweight, header-only library that enables seamless interoperability between C++ and Python. It allows you to expose C++ classes, functions, and data structures to Python, making it easy to call C++ code from Python scripts and vice versa.

## Why use pybind11?

- **Performance**: Leverage C++ speed for computationally intensive tasks while maintaining Python's ease of use.
- **Integration**: Easily wrap existing C++ libraries for use in Python applications.
- **Simplicity**: Minimal boilerplate; header-only design means no separate compilation step for the binding code.
- **Maintainability**: Clean, readable syntax for binding code, reducing maintenance overhead.
- **Community**: Widely used in scientific computing, machine learning, and production systems.

## How does pybind11 work?

pybind11 uses C++11 features to create bindings. You write C++ code that describes how your classes/functions should be exposed to Python, then compile it into a Python extension module.

### Basic Steps
1. **Install pybind11**: `pip install pybind11` or use as a submodule in your C++ project.
2. **Write C++ binding code**: Use pybind11 macros to expose functions/classes.
3. **Build the extension**: Use CMake, setuptools, or other build tools to compile the module.
4. **Import in Python**: Use the generated module like any other Python package.

## Example 1: Exposing a Simple Function

```cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

int add(int i, int j) {
	return i + j;
}

PYBIND11_MODULE(example, m) {
	m.def("add", &add, "A function that adds two numbers");
}
```

Build with CMake or setuptools, then use in Python:

```python
import example
print(example.add(2, 3))  # Output: 5
```

## Example 2: Exposing a C++ Class

```cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

class Pet {
public:
	Pet(const std::string &name) : name(name) {}
	void setName(const std::string &name_) { name = name_; }
	const std::string &getName() const { return name; }
private:
	std::string name;
};

PYBIND11_MODULE(example, m) {
	py::class_<Pet>(m, "Pet")
		.def(py::init<const std::string &>())
		.def("setName", &Pet::setName)
		.def("getName", &Pet::getName);
}
```

Python usage:
```python
import example
dog = example.Pet("Fido")
print(dog.getName())  # Output: Fido
dog.setName("Rex")
print(dog.getName())  # Output: Rex
```

## Example 3: Wrapping a C++ Library for Production

Suppose you have a C++ image processing library. You can expose its functions to Python for rapid prototyping and integration with ML workflows:

```cpp
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "image_lib.h" // Your C++ library
namespace py = pybind11;

py::array_t<uint8_t> process_image(py::array_t<uint8_t> input) {
	// ... call C++ code to process image ...
}

PYBIND11_MODULE(imgproc, m) {
	m.def("process_image", &process_image);
}
```

## How pybind11 Saves Time, Effort, and Money

- **Reuse Existing Code**: No need to rewrite C++ libraries in Python; wrap and reuse.
- **Rapid Prototyping**: Python bindings allow fast experimentation and integration with Python's rich ecosystem (NumPy, pandas, ML frameworks).
- **Performance Optimization**: Move bottlenecks to C++ without changing the Python API.
- **Reduced Maintenance**: Clean, minimal binding code means less to debug and maintain.
- **Cost Savings**: Faster development cycles and better resource utilization (engineers can work in their preferred language).

## References
- [pybind11 official docs](https://pybind11.readthedocs.io/en/stable/)
- [pybind11 GitHub](https://github.com/pybind/pybind11)

---
For more advanced examples (custom types, NumPy arrays, STL containers, etc.), see the official documentation.

# ⚡ Usecase: True Parallelism with `multiprocessing`

Your computer has multiple CPU cores, but by default, a standard Python program only runs on one at a time. This is because of a mechanism called the **Global Interpreter Lock (GIL)**, which prevents multiple threads from executing Python bytecode simultaneously.

So, how do you make your Python code truly run in parallel to take full advantage of modern hardware for CPU-intensive tasks (like data processing, mathematical computations, or video encoding)? The answer is the `multiprocessing` module.

## 🗺️ A Mind Map of the `multiprocessing` Module

The `multiprocessing` module provides a suite of tools for creating and managing parallel processes.

```mermaid
mindmap
  root((`multiprocessing`))
    --> Core Concepts
      --> Bypasses the GIL for true parallelism
      --> Each process has its own memory
      --> Best for **CPU-Bound** tasks
    --> Creating Processes
      --> `Process` class
    --> Distributing Work
      --> `Pool`
    --> Sharing Data & Communicating
      --> `Queue` (Process-safe)
      --> `Pipe` (Two-way communication)
      --> Shared Memory (`Value`, `Array`)
    --> Synchronization
      --> `Lock` (Prevent race conditions)
```

---

## 🤔 What Is `multiprocessing`?

The `multiprocessing` module allows you to spawn new processes, each with its own Python interpreter and memory space. Because each process has its own interpreter, it is not subject to the GIL of the main process, meaning they can all run on different CPU cores at the same time.

This makes it the ideal tool for **CPU-bound** work—tasks where the limiting factor is the speed of the CPU, not waiting for external resources like a network or a hard drive.

## ✨ Why Is `multiprocessing` So Important?

*   **Bypasses the GIL:** This is the main reason it exists. It's Python's built-in solution for achieving true parallelism.
*   **Maximizes CPU Utilization:** It allows you to scale your application across all available CPU cores, dramatically speeding up heavy computations.
*   **Robustness:** Since processes have separate memory, a crash in one process won't affect the others or the main application.

The main trade-off is that sharing data between processes is more complex than with threads, as they don't share memory. You have to use explicit communication mechanisms like Queues or Pipes.

---

## 🚀 How Do I Use `multiprocessing`?

Let's explore the fundamental patterns.

### The `if __name__ == '__main__':` Guard

You will see this in almost every multiprocessing script. When a new process is spawned, it re-imports the script. This guard ensures that the process-spawning code only runs once in the main process, preventing an infinite loop of new processes. **You must use this on platforms like Windows and macOS.**

```python
if __name__ == '__main__':
  # Your multiprocessing code goes here
  pass
```

### 1. Creating and Running a Basic Process

The `Process` class is the fundamental building block. You give it a `target` function to run.

```python
import multiprocessing
import os
import time

def worker_function(task_name):
  """A simple function that a process can run."""
  print(f"Starting task: {task_name} (Process ID: {os.getpid()})")
  time.sleep(2)
  print(f"Finished task: {task_name}")

if __name__ == '__main__':
  print(f"Main process ID: {os.getpid()}")

  # Create two Process objects
  p1 = multiprocessing.Process(target=worker_function, args=("Task A",))
  p2 = multiprocessing.Process(target=worker_function, args=("Task B",))

  # Start the processes (they will run in parallel)
  p1.start()
  p2.start()

  print("Main process is waiting for child processes to finish...")

  # Wait for the processes to complete before exiting the script
  p1.join()
  p2.join()

  print("All tasks are done!")
```

### 2. Distributing Tasks with a `Pool`

Creating and managing individual processes can be tedious. A `Pool` object manages a fixed number of worker processes for you and can easily distribute a large number of tasks among them.

The `pool.map()` function is perfect for this. It takes a function and an iterable, applies the function to each item in the iterable in parallel, and returns a list of the results.

```python
import multiprocessing

def square(n):
  return n * n

if __name__ == '__main__':
  # Create a pool of 4 worker processes
  with multiprocessing.Pool(processes=4) as pool:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    results = pool.map(square, numbers)

  print(f"Original numbers: {numbers}")
  print(f"Squared results: {results}")
```

### 3. Sharing Data with a `Queue`

Since processes don't share memory, you need a way to pass data between them. A `multiprocessing.Queue` is a process-safe way to do this. One process can `.put()` data onto the queue, and another can `.get()` it.

```python
import multiprocessing

def data_producer(q):
  """This function puts data into the queue."""
  print("Producer sending data...")
  q.put([42, None, "hello"])
  print("Producer is done.")

def data_consumer(q):
  """This function gets data from the queue."""
  print("Consumer waiting for data...")
  data = q.get()
  print(f"Consumer received: {data}")

if __name__ == '__main__':
  queue = multiprocessing.Queue()

  p_producer = multiprocessing.Process(target=data_producer, args=(queue,))
  p_consumer = multiprocessing.Process(target=data_consumer, args=(queue,))

  p_producer.start()
  p_consumer.start()

  p_producer.join()
  p_consumer.join()
```
When you need to max out your CPU for heavy computational tasks, `multiprocessing` is the right tool for the job.

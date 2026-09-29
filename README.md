# Persistent Priority Queue

A Python implementation of a **Min-Heap based Priority Queue** with **PostgreSQL persistence**.

The project supports both in-memory and persistent queue operations. When persistence is enabled, queue elements are stored in PostgreSQL and automatically restored when a new queue instance is created.

---

## Features

* Binary Min-Heap implementation
* Insert elements into the queue
* Peek at the minimum element without removing it
* Extract the minimum element
* Check whether the queue is empty
* PostgreSQL persistence
* Restore queue state after creating a new queue instance
* Automated unit tests using pytest
* Environment-based database configuration
* Clean separation between heap logic and database storage

---

## Technology Stack

| Technology    | Purpose                                       |
| ------------- | --------------------------------------------- |
| Python        | Application and data structure implementation |
| PostgreSQL    | Persistent queue storage                      |
| psycopg       | PostgreSQL database connectivity              |
| python-dotenv | Environment variable management               |
| pytest        | Automated testing                             |
| Git           | Version control                               |

---

## Project Structure

```text
SARALWEB_assignment/
│
├── .env
├── .gitignore
├── README.md
├── db.py
├── pytest.ini
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   │
│   └── priority_queue/
│       ├── __init__.py
│       ├── heap.py
│       └── storage.py
│
└── tests/
    └── test_heap.py
```

### File Responsibilities

#### `db.py`

Responsible for creating PostgreSQL database connections using the `DATABASE_URL` environment variable.

#### `src/priority_queue/heap.py`

Contains the `MinHeap` implementation.

Responsibilities include:

* Insert
* Peek
* Extract minimum
* Heap maintenance
* Optional persistence integration

#### `src/priority_queue/storage.py`

Contains the `QueueStorage` class.

Responsibilities include:

* Save queue items to PostgreSQL
* Load persisted queue items
* Remove queue items
* Clear queue storage

#### `tests/test_heap.py`

Contains automated tests for:

* Empty queue
* Min-heap insertion
* Peek
* Extract minimum
* Persistence across queue instances
* Loading persisted items

---

# How the Min-Heap Works

The queue is implemented using a binary Min-Heap.

For an element at index `i`, its relationships are:

```text
Parent       = (i - 1) // 2
Left Child   = 2 * i + 1
Right Child  = 2 * i + 2
```

The smallest element is always maintained at index `0`.

For example, inserting:

```text
10
5
7
1
```

results in:

```text
        1
       / \
      5   7
     /
    10
```

The internal array representation is:

```text
[1, 5, 7, 10]
```

---

# Queue Operations

## Insert

When an item is inserted:

1. The item is added to the end of the array.
2. It is compared with its parent.
3. If it is smaller than the parent, the two elements are swapped.
4. This continues until the Min-Heap property is restored.

### Time Complexity

```text
O(log n)
```

---

## Peek

Returns the smallest element without removing it.

Since the minimum element is always at index `0`:

```text
O(1)
```

---

## Extract Minimum

The minimum element is removed from the queue.

The last element is moved to the root and the heap is restored using heapification.

### Time Complexity

```text
O(log n)
```

---

## Check Empty

Checks whether the queue contains any elements.

### Time Complexity

```text
O(1)
```

---

# PostgreSQL Persistence

The queue supports an optional persistent mode.

A normal queue can be created using:

```python
from src.priority_queue.heap import MinHeap

heap = MinHeap()
```

A persistent queue can be created using:

```python
heap = MinHeap(persistent=True)
```

When persistent mode is enabled:

```text
              MinHeap
                 │
        ┌────────┴────────┐
        │                 │
 In-memory Heap     QueueStorage
                          │
                          ▼
                     PostgreSQL
```

Insert operations store the item in PostgreSQL.

Extract operations remove the corresponding item from PostgreSQL.

When another persistent `MinHeap` instance is created, the stored items are loaded from PostgreSQL and the heap is rebuilt.

---

# Database Schema

The project uses a PostgreSQL table named `queue_items`.

```sql
CREATE TABLE queue_items (
    id BIGSERIAL PRIMARY KEY,
    item TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Columns

| Column       | Type          | Description                     |
| ------------ | ------------- | ------------------------------- |
| `id`         | `BIGSERIAL`   | Unique queue item identifier    |
| `item`       | `TEXT`        | Stored queue value              |
| `created_at` | `TIMESTAMPTZ` | Time when the item was inserted |

The `id` column preserves insertion order when loading stored items.

---

# Requirements

The project requires:

* Python 3.10 or newer
* PostgreSQL
* pip
* Git

The project has been tested with:

```text
Python 3.14.6
PostgreSQL
pytest 9.1.1
```

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd SARALWEB_assignment
```

---

## 2. Create a Virtual Environment

Windows:

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_string
```

The application reads the database connection using `python-dotenv`.

### Important

The `.env` file contains sensitive database credentials and must not be committed to Git.

The repository includes `.env` in `.gitignore`.

---

# Database Setup

Create the required PostgreSQL table:

```sql
CREATE TABLE queue_items (
    id BIGSERIAL PRIMARY KEY,
    item TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

The application will then use this table for persistent queue operations.

---

# Usage

## In-Memory Queue

```python
from src.priority_queue.heap import MinHeap

heap = MinHeap()

heap.insert(10)
heap.insert(5)
heap.insert(7)
heap.insert(1)

print(heap.peek())
```

Output:

```text
1
```

Extract the minimum:

```python
print(heap.extract_min())
```

Output:

```text
1
```

The remaining heap is:

```text
[5, 10, 7]
```

---

# Persistent Queue

Create a persistent queue:

```python
from src.priority_queue.heap import MinHeap

heap = MinHeap(persistent=True)

heap.insert(10)
heap.insert(5)
heap.insert(7)
heap.insert(1)

print(heap.peek())
```

Output:

```text
1
```

Extract the minimum:

```python
print(heap.extract_min())
```

Output:

```text
1
```

The remaining elements are persisted in PostgreSQL.

---

# Persistence Across Queue Instances

One of the main requirements of the project is that queue data should survive creation of a new queue instance.

Example:

```python
from src.priority_queue.heap import MinHeap

heap = MinHeap(persistent=True)

heap.insert(10)
heap.insert(5)
heap.insert(7)
heap.insert(1)

print(heap.extract_min())
```

Output:

```text
1
```

Now create a completely new queue instance:

```python
new_heap = MinHeap(persistent=True)

print(new_heap.peek())
```

Output:

```text
5
```

The new queue loads the remaining items from PostgreSQL.

Conceptually:

```text
Queue Instance 1
       │
       │ insert
       ▼
PostgreSQL
       │
       │ new queue instance
       ▼
Queue Instance 2
       │
       ▼
Restored Heap
```

---

# Testing

The project uses `pytest`.

Run the complete test suite from the project root:

```cmd
pytest -v
```

The current test suite contains six tests.

Expected result:

```text
6 passed
```

---

# Test Coverage

The tests verify the following behavior.

## 1. New Queue Is Empty

```python
def test_new_heap_is_empty():
    heap = MinHeap()

    assert heap.is_empty() is True
```

---

## 2. Insert Maintains Min-Heap

```python
def test_insert_maintains_min_heap():
    heap = MinHeap()

    heap.insert(10)
    heap.insert(5)
    heap.insert(7)
    heap.insert(1)

    assert heap.heap == [1, 5, 7, 10]
```

---

## 3. Peek Returns Minimum

The `peek()` operation returns the minimum without modifying the queue.

---

## 4. Extract Minimum

The `extract_min()` operation returns the smallest element and restores the heap.

---

## 5. Persistence Survives Restart

The test creates one persistent queue, inserts elements, extracts an element, and creates a new queue instance.

The second queue must load the remaining elements from PostgreSQL.

---

## 6. Existing Persistent Items Are Loaded

The test verifies that a new persistent queue correctly loads items that already exist in PostgreSQL.

---

# Example Test Result

The current test suite passes:

```text
============================= test session starts =============================

collected 6 items

tests/test_heap.py::test_new_heap_is_empty PASSED
tests/test_heap.py::test_insert_maintains_min_heap PASSED
tests/test_heap.py::test_peek_returns_minimum_without_removing PASSED
tests/test_heap.py::test_extract_min_returns_smallest_and_maintains_heap PASSED
tests/test_heap.py::test_persistent_queue_survives_restart PASSED
tests/test_heap.py::test_persistent_queue_loads_existing_items PASSED

============================== 6 passed ==============================
```

---

# Complexity Analysis

| Operation                       | Time Complexity |
| ------------------------------- | --------------: |
| `insert()`                      |        O(log n) |
| `peek()`                        |            O(1) |
| `extract_min()`                 |        O(log n) |
| `is_empty()`                    |            O(1) |
| Build heap from persisted items |            O(n) |

The heap operations maintain the standard binary Min-Heap complexity.

Database operations additionally depend on PostgreSQL connection and query execution time.

---

# Design Overview

The implementation separates responsibilities into three layers.

```text
┌──────────────────────────────┐
│          MinHeap             │
│                              │
│ insert / peek / extract      │
│ heap maintenance             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       QueueStorage           │
│                              │
│ save / load / remove / clear │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         PostgreSQL           │
│                              │
│        queue_items           │
└──────────────────────────────┘
```

This separation keeps the heap algorithm independent from the database implementation while allowing persistence to be enabled when required.

---

# Git Configuration

The following files and directories should not be committed:

```text
.env
.venv/
.pytest_cache/
__pycache__/
.vscode/
```

They are excluded through `.gitignore`.

The source code, tests, configuration, dependency file, and README should be committed.

Before committing, verify:

```cmd
git status
```

Make sure `.env` is not listed as a tracked file.

---

# Running the Project

The complete workflow is:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

If all tests pass, the implementation is ready for submission.

---

# Conclusion

This project implements a persistent Min-Heap based Priority Queue using Python and PostgreSQL.

The implementation provides:

* Efficient priority queue operations
* Standard Min-Heap behavior
* Optional PostgreSQL persistence
* Queue restoration across instances
* Automated testing
* Separation between data structure and persistence layers
* Environment-based database configuration
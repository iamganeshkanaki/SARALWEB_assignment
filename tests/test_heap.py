from src.priority_queue.heap import MinHeap


def test_new_heap_is_empty():
    heap = MinHeap()

    assert heap.is_empty() is True


def test_insert_maintains_min_heap():
    heap = MinHeap()

    heap.insert(10)
    heap.insert(5)
    heap.insert(7)
    heap.insert(1)

    assert heap.heap == [1, 5, 7, 10]


def test_peek_returns_minimum_without_removing():
    heap = MinHeap()

    heap.insert(10)
    heap.insert(5)
    heap.insert(7)
    heap.insert(1)

    assert heap.peek() == 1
    assert heap.heap == [1, 5, 7, 10]


def test_extract_min_returns_smallest_and_maintains_heap():
    heap = MinHeap()

    heap.insert(10)
    heap.insert(5)
    heap.insert(7)
    heap.insert(1)

    assert heap.extract_min() == 1
    assert heap.heap == [5, 10, 7]


def test_persistent_queue_survives_restart():
    heap = MinHeap(persistent=True)

    heap.storage.clear()
    heap.heap.clear()

    heap.insert(10)
    heap.insert(5)
    heap.insert(7)
    heap.insert(1)

    assert heap.peek() == 1
    assert heap.extract_min() == 1

    new_heap = MinHeap(persistent=True)

    assert new_heap.heap == [5, 10, 7]
    assert new_heap.peek() == 5

    new_heap.storage.clear()


def test_persistent_queue_loads_existing_items():
    heap = MinHeap(persistent=True)

    heap.storage.clear()
    heap.heap.clear()

    heap.insert(30)
    heap.insert(10)
    heap.insert(20)

    new_heap = MinHeap(persistent=True)

    assert new_heap.peek() == 10
    assert sorted(new_heap.heap) == [10, 20, 30]

    new_heap.storage.clear()
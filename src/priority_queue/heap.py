from .storage import QueueStorage


class MinHeap:

    def __init__(self, persistent=False):
        self.heap = []
        self.storage = QueueStorage() if persistent else None

        if self.storage:
            self.heap = self._load_from_storage()

            # Build the heap from persisted values
            for index in range(len(self.heap) // 2 - 1, -1, -1):
                self._heapify_down(index)

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, item):
        self.heap.append(item)

        current_index = len(self.heap) - 1

        while current_index > 0:
            parent_index = (current_index - 1) // 2

            if self.heap[current_index] >= self.heap[parent_index]:
                break

            self.heap[current_index], self.heap[parent_index] = (
                self.heap[parent_index],
                self.heap[current_index],
            )

            current_index = parent_index

        if self.storage:
            self.storage.save(item)

    def peek(self):
        if self.is_empty():
            return None

        return self.heap[0]

    def extract_min(self):
        if self.is_empty():
            return None

        minimum = self.heap[0]

        if len(self.heap) == 1:
            self.heap.pop()

            if self.storage:
                self.storage.remove(minimum)

            return minimum

        self.heap[0] = self.heap.pop()

        self._heapify_down(0)

        if self.storage:
            self.storage.remove(minimum)

        return minimum

    def _heapify_down(self, current_index):
        while True:
            left_child_index = 2 * current_index + 1
            right_child_index = 2 * current_index + 2

            smallest_index = current_index

            if (
                left_child_index < len(self.heap)
                and self.heap[left_child_index] < self.heap[smallest_index]
            ):
                smallest_index = left_child_index

            if (
                right_child_index < len(self.heap)
                and self.heap[right_child_index] < self.heap[smallest_index]
            ):
                smallest_index = right_child_index

            if smallest_index == current_index:
                break

            self.heap[current_index], self.heap[smallest_index] = (
                self.heap[smallest_index],
                self.heap[current_index],
            )

            current_index = smallest_index

    def _load_from_storage(self):
        return self.storage.load_all()
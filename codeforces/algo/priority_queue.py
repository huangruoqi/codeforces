from typing import Callable, Any, Optional


class PQ:
    def __init__(self, arr=None):
        self.arr = []
        if arr is not None:
            self.arr = sorted(arr)

    def push(self, item):
        self.arr.append(item)
        self.arr.sort()

    def peek(self):
        return self.arr[-1]

    def pop(self):
        return self.arr.pop()

    def empty(self):
        return len(self.arr) == 0


class Heap:
    def __init__(self, arr=None, compare_func: Callable[[Any, Any], int] = None):
        self.arr = arr or []
        self.compare_func = compare_func
        self.heapify()

    def swap(self, i1, i2):
        self.arr[i1], self.arr[i2] = self.arr[i2], self.arr[i1]

    def compare(self, i1, i2):
        return self.compare_func(self.arr[i1], self.arr[i2])

    def push(self, item):
        index = len(self.arr)
        self.arr.append(item)
        while index > 0:
            parent_index = (index - 1) // 2
            compare_parent = self.compare(index, parent_index)
            if compare_parent < 0:
                self.swap(index, parent_index)
                index = parent_index
            else:
                break

    def pop(self):
        self.swap(0, len(self.arr) - 1)
        item = self.arr.pop()
        self.reheap_down(0)
        return item

    def reheap_down(self, index):
        smallest = index
        left = index * 2 + 1
        right = left + 1
        n = len(self.arr)
        if left < n:
            compare_left = self.compare(left, smallest)
            if compare_left < 0:
                smallest = left
        if right < n:
            compare_right = self.compare(right, smallest)
            if compare_right < 0:
                smallest = right
        if smallest != index:
            self.swap(smallest, index)
            self.reheap_down(smallest)

    def heapify(self):
        for i in range(len(self.arr) // 2 - 1, -1, -1):
            self.reheap_down(i)

    def empty(self):
        return len(self.arr) == 0

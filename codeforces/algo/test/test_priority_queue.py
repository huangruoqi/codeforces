import random
import pytest
from ..priority_queue import PQ, Heap


def test_pq_init():
    pq = PQ()
    assert pq.empty()


def test_pq_sort():
    NUM = 100
    arr = random.sample(list(range(NUM)), k=NUM)
    sorted_arr = sorted(arr, reverse=True)
    pq = PQ(arr)
    temp_arr = [pq.pop() for _ in range(NUM)]

    assert temp_arr == sorted_arr
    with pytest.raises(Exception):
        pq.pop()


def test_heap_sort():
    NUM = 100
    arr = random.sample(list(range(NUM)), k=NUM)
    sorted_arr = sorted(arr, reverse=True)
    pq = Heap(arr, compare_func=lambda a, b: b - a)
    temp_arr = [pq.pop() for _ in range(NUM)]
    assert len(temp_arr) == len(sorted_arr)
    assert temp_arr == sorted_arr
    with pytest.raises(Exception):
        pq.pop()


def test_pq_sort():
    NUM = 100
    arr = random.sample(list(range(NUM)), k=NUM)
    sorted_arr = sorted(arr, reverse=True)
    pq = PQ(arr)
    temp_arr = [pq.pop() for _ in range(NUM)]
    assert len(temp_arr) == len(sorted_arr)
    assert temp_arr == sorted_arr
    with pytest.raises(Exception):
        pq.pop()

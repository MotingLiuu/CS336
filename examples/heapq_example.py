import heapq
import argparse

'''
heap[k] <= heap[2*k + 1] and heap[k] <= heap[2*k + 2]
1. zero-based indexing
2. pop returns the smallest item

heapq.heappush(heap, item)

heapq.heappop(heap)

heapq.heappushpop(heap, item)

heapq.heapify(x)
Transform list x into a heap, in-place, in linear time.

heapq.heapreplace(heap, item)

heapq.merge(*iterables, key=None, reverse=False)
Merge multiple sorted inputs into a single sorted output (for example, merge timestamped entries from multiple log files). Returns an iterator over the sorted values.


'''

# =======
# HeapSort
# =======

def example_sort():
    def heapsort(iterable):
        h = []
        for value in iterable:
            heapq.heappush(h, value)
        return [heapq.heappop(h) for i in range(len(h))]
    print(heapsort([5, 3, 1, 22, 11, 4, 1]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='heap examples')
    parser.add_argument(
        'example',
        choices = ['heapsort'],
        help = 'Select one example to run'
    )
    args = parser.parse_args()
    
    if args.example == 'heapsort':
        example_sort()
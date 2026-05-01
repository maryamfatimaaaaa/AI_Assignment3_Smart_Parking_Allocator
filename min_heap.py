class MinHeap:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def push(self, node):
        self.heap.append(node)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        min_node = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return min_node

    def _bubble_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx].f < self.heap[parent].f:
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            else:
                break

    def _bubble_down(self, idx):
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < len(self.heap) and self.heap[left].f < self.heap[smallest].f:
                smallest = left
            if right < len(self.heap) and self.heap[right].f < self.heap[smallest].f:
                smallest = right
            if smallest != idx:
                self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
                idx = smallest
            else:
                break

    def __contains__(self, node):
        return any(n.row == node.row and n.col == node.col for n in self.heap)
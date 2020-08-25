from abc import ABC, abstractmethod
import heapq


class DataStruct(ABC):
    """Defines an abstract interface for data structures to be used in search methods"""

    def __init__(self):
        self.list = []

    @abstractmethod
    def push(self, item, priority=None):
        """Push the given item into the data structure"""
        pass

    def pop(self):
        """Pop an item out of the data structure"""
        return self.list.pop()

    def is_empty(self):
        """Returns True iff the data structure is free of any item"""
        return len(self.list) == 0


class Queue(DataStruct):
    """
    Implements a simple Queue data structure.
    A queue uses the First-in-First-out paradigm
    """

    def push(self, item, priority=None):
        self.list.insert(0, item)


class Stack(DataStruct):
    """
    Implements a simple Stack data structure.
    A stack uses the First-in-Last-out paradigm
    """

    def push(self, item, priority=None):
        self.list.append(item)


class PriorityQueue(DataStruct):
    """
    Implements a priority queue data structure.
    The queue will store each item with a paired priority. That way,
    when the pop() method is called, the queue will return the item with
    the lowest priority
    """

    def __init__(self):
        super().__init__()
        self.init = False

    def push(self, item, priority=None):
        if not self.init:
            self.init = True
            try:
                item < item
            except:
                item.__class__.__lt__ = lambda x, y: (True)
        pair = (priority, item)
        heapq.heappush(self.list, pair)

    def pop(self):
        priority, item = heapq.heappop(self.list)
        return item

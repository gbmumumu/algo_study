#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from queue import Queue
from random import choice


class BFS:
    def __init__(self, gph,
                 assign_start='',
                 assign_end=''):
        self.graph = gph
        self.queue = Queue()
        self.visited = []
        keys = list(self.graph.keys()).copy()
        if not (assign_start and assign_end):
            self.start = self._get_point(assign_start, keys)
            keys.remove(self.start)
            self.end = self._get_point(assign_end, keys)
        else:
            self.start = assign_start
            self.end = assign_end
        self.fd = {self.start: None}

    @staticmethod
    def _get_point(point_name, key_lst):
        return choice(list(key_lst))


    def run_bfs(self):
        self.queue.put(self.start)
        self.visited.append(self.start)
        while not self.queue.empty():
            vertex = self.queue.get()
            nodes = self.graph[vertex]
            for inode in nodes:
                if inode not in self.visited:
                    self.queue.put(inode)
                    self.visited.append(inode)
                    self.fd[inode] = vertex
            # print(vertex)
        return self.fd

    def _shortest_path(self):
        # for k, v in self.fd.items():
        #     print('child: {} -> parent: {}'.format(k, v))
        # print(self.fd)
        self.run_bfs()
        node = self.end
        path = []
        while node is not None:
            path.append(node)
            node = self.fd[node]
        return list(reversed(path))

    def __repr__(self):
        return "The shortest path is:" + "->".join(self._shortest_path())

    def __len__(self):
        return len(self._shortest_path()) - 1

    def get_shortest_path(self):
        print("start from {} to {}".format(self.start, self.end))
        print(repr(self))
        print("The step is: ", len(self))
        return self._shortest_path()


if __name__ == "__main__":
    graph = {
        "CAB": ["CAT", "CAR"],
        "CAR": ["CAB", "CAT", "BAR"],
        "CAT": ["CAB", "CAR", "MAT", "BAT"],
        "MAT": ["CAT", "BAT"],
        "BAT": ["MAT", "CAT", "BAR"],
        "BAR": ["CAR", "BAT"]
    }
    t = BFS(graph, assign_start='CAB', assign_end='BAT')
    t.get_shortest_path()

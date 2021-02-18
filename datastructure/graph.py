#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# ADT Graph
# add vertex; add edge; get vertex, in;
# adjacency matrix 邻接矩阵
# adjacency list 邻接表

# adjacency matrix
# 边数很少则效率低下： -> 稀疏sparse矩阵，大多数问题的边远远小于 V^2, 都是稀疏的
# 因此引出了邻接列表
# 存储空间紧凑且高效，容易获得顶点和边的信息

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connected_to = {}

    def add_neighbor(self, nbr, weight=0):
        self.connected_to[nbr] = weight

    def __str__(self):
        return str(self.id) + 'connected to:' \
               + str([x.id for x in self.connected_to])

    def get_connections(self):
        return self.connected_to.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr):
        return self.connected_to[nbr]


class Graph:
    def __init__(self):
        self.vert_lst = {}
        self.num_of_vertices = 0

    def add_vertex(self, key):
        self.num_of_vertices += 1
        new_vertex = Vertex(key)
        self.vert_lst[key] = new_vertex

        return new_vertex

    def get_vertex(self, key):
        if key in self.vert_lst:
            return self.vert_lst[key]
        return None

    def __contains__(self, item):
        return item in self.vert_lst

    def add_edge(self, f, t, cost=0):
        if f not in self.vert_lst:
            self.add_vertex(f)
        if t not in self.vert_lst:
            self.add_vertex(t)
        self.vert_lst[f].add_neighbor(self.vert_lst[t], cost)

    def get_vertices(self):
        return self.vert_lst.keys()

    def __iter__(self):
        return iter(self.vert_lst.values())


# app
# Word Ladder 词梯问题
# 将可能的单词之间的演变关系表达为图
# 广度优先搜索BFS，来搜寻开始单词到结束单词之间的所有有效路径
# 选择其中最快的路径

# 将单词作为标识key，若单词相差一个字母，则在它们之间设一条边
# FOOL -> SAGE
# 创建大量的桶
def build_graph(word_file):
    d = {}
    g = Graph()
    with open(word_file, "r") as f:
        for line in f:
            word = line[:-1]
            for i in range(len(word)):
                bucket = word[:i] + '_' + word[i + 1:]
                if bucket in d:
                    d[bucket].append(word)
                else:
                    d[bucket] = [word]
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.add_edge(word1, word2)

    return g


def bfs(g, start):
    pass


# 骑士周游问题
def legal_coord(c, bd_size):
    return 0 <= c < bd_size


def get_legal_move(x, y, bd_size):
    new_moves = []
    move_offsets = [
        (-1, -2), (-1, 2), (-2, -1), (-2, 1),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    for i in move_offsets:
        new_x = x + i[0]
        new_y = y + i[0]
        if legal_coord(new_x, bd_size) and legal_coord(new_y, bd_size):
            new_moves.append((new_x, new_y))

    return new_moves


def pos_to_node_id(row, col, bd_size):
    return row * bd_size + col


def knight_graph(bd_size):
    kt_graph = Graph()
    for row in range(bd_size):
        for col in range(bd_size):
            node_id = pos_to_node_id(row, col, bd_size)
            new_pos = get_legal_move(row, col, bd_size)
            for e in new_pos:
                nid = pos_to_node_id(e[0], e[1], bd_size)
                kt_graph.add_edge(node_id, nid)

    return kt_graph


if __name__ == "__main__":
    pass

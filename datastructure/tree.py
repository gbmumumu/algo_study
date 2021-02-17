#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# node
# edge
# root
# path
# children
# parent
# subtree
# sibling (兄弟节点)
# leaf 叶节点
# Level
# 高度， 所有节点的最大层级

# >>>>>树的定义：
# 树由若干接点，以及两两连接节点的边组成
# 其中一个节点被设为根节点
# 每个节点n，都恰连接一条来自节点p的边，p是n的父节点
# 如果每个节点最多两个子节点，这样的树被称为二叉树

# 空集 树，
# 由根节点及0或多个子树构成，其中子树也是树，
# 字数的根到根节点具有边相连

# 嵌套列表实现：
# [root, left, right], 一种递归数据结构，
# 很容易扩展到多茶树，仅需要增加列表元素即可
my_tree = [
    'a', ['b', []], ['c', []]
]


def binary_tree(r):
    return [r, [], []]


def insert_left(root, new_branch):
    t = root.pop(1)
    if len(t) > 1:
        root.insert(1, [new_branch, t, []])
    else:
        root.insert(1, [new_branch, [], []])

    return root


def insert_right(root, new_branch):
    t = root.pop(2)
    if len(t) > 1:
        root.insert(2, [new_branch, [], t])
    else:
        root.insert(2, [new_branch, [], []])

    return root


def get_root_val(root):
    return root[0]


def set_root_val(root, new_val):
    root[0] = new_val


def get_left_children(root):
    return root[1]


def get_right_children(root):
    return root[2]


r = binary_tree(3)
insert_left(r, 4)
insert_left(r, 5)
insert_right(r, 6)
insert_right(r, 7)
print(r)
l = get_left_children(r)
set_root_val(l, 9)
print(l)


# 节点链接法
class BinaryTree:
    def __init__(self, root_obj):
        self.key = root_obj
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        if self.left_child is None:
            self.left_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        if self.right_child is None:
            self.right_child = BinaryTree(new_node)
        else:
            t = BinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_val(self, obj):
        self.key = obj

    def get_root_val(self):
        return self.key


r = BinaryTree('a')
r.insert_left('b')
r.insert_right('c')
r.get_right_child().set_root_val('hello')
r.get_left_child().insert_right('d')

# app
# 表达式解析
# 语法分析树
# 机器翻译，语义理解
_expr = '( 3 + ( 4 * 5 ) )'
my_expr = _expr.split()


def build_parser_tree(expr: list):
    from LinearStructure import Stack
    p_stack = Stack()
    e_tree = BinaryTree('')
    p_stack.push(e_tree)
    cur_tree = e_tree
    for i in expr:
        if i == '(':
            cur_tree.insert_left('')
            p_stack.push(cur_tree)
            cur_tree = cur_tree.get_left_child()
        elif i.isdigit():
            cur_tree.set_root_val(int(i))
            parent = p_stack.pop()
            cur_tree = parent
        elif i in ['+', '-', '*', '/']:
            cur_tree.set_root_val(i)
            cur_tree.insert_right('')
            p_stack.push(cur_tree)
            cur_tree = cur_tree.get_right_child()
        elif i == ')':
            cur_tree = p_stack.pop()
        else:
            raise ValueError
    return e_tree


expr_tree = build_parser_tree(my_expr)


# 求值
# 函数引用


def evaluate(tree: BinaryTree):
    import operator
    opers = {'+': operator.add, '-': operator.sub,
             '*': operator.mul, '/': operator.truediv}
    left_tree = tree.get_left_child()
    right_tree = tree.get_right_child()
    if left_tree and right_tree:
        fn = opers[tree.get_root_val()]
        return fn(evaluate(left_tree), evaluate(right_tree))
    else:
        return tree.get_root_val()


results = evaluate(expr_tree)
print(my_expr)
print(results)


# 树的遍历
# 前序遍历
# ->根 ->左 ->右
# 中序遍历
# ->左 ->根 ->右
# 后序遍历
# ->左 ->右 ->根

def per_order(tree: BinaryTree):  # 前序遍历
    if tree:
        print(tree.get_root_val())
        per_order(tree.get_left_child())
        per_order(tree.get_right_child())


def post_order(tree: BinaryTree):  # 后序遍历
    if tree is not None:
        post_order(tree.get_left_child())
        post_order(tree.get_right_child())
        print(tree.get_root_val())


def in_order(tree: BinaryTree):  # 中序遍历
    if tree is not None:
        in_order(tree.get_left_child())
        print(tree.get_root_val())
        in_order(tree.get_right_child())


def print_expr(tree: BinaryTree):
    s_val = ''
    if tree:
        s_val = '(' + print_expr(tree.get_left_child())
        s_val = s_val + str(tree.get_root_val())
        s_val = s_val + print_expr(tree.get_right_child()) + ')'
    return s_val


# 优先队列
# priority queue
# 二叉堆 O(log n)
# 最小堆/大堆
# ADT: BinaryHeap
# insert, findMin, delMin, is_empty, size, buildHeap
# 采用完全二叉树的结构近似实现"平衡"
# 如果节点下表为p，左子节点下标为2p，右子节点下标为2p+1，父节点为p//2
# 任何一个节点x， 其父节点p中的key均小于x中的key
# -> 根节点k最小

class BinaryHeap:
    def __init__(self):
        self.heap_list = [0]  # 无需进行下标的偏移值操作
        self.cur_size = 0

    def perc_up(self, i):  # 上浮
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]:
                tmp = self.heap_list[i // 2]
                self.heap_list[i // 2] = self.heap_list[i]
                self.heap_list[i] = tmp
            i //= 2

    def insert(self, key):
        self.heap_list.append(key)
        self.cur_size += 1
        self.perc_up(self.cur_size)

    def min_child(self, i):
        if i * 2 + 1 > self.cur_size:
            return i * 2
        else:
            if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:
                return i * 2 + 1

    def perc_down(self, i):
        while i * 2 <= self.cur_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                tmp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            i = mc

    def del_min(self):
        ret_val = self.heap_list[1]  # 移走堆顶
        self.heap_list[1] = self.heap_list[self.cur_size]
        self.cur_size -= 1
        self.heap_list.pop()
        self.perc_down(1)  # 新顶下沉
        return ret_val

    def build_heap(self, lst):   # O(n)
        i = len(lst) // 2
        self.cur_size = len(lst)
        self.heap_list = [0] + lst
        while i > 0:
            self.perc_down(i)
            i -= 1

# 堆排序 O(n log n)
# pass
# 二叉查找树


if __name__ == "__main__":
    pass

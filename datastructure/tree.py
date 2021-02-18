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

    def build_heap(self, lst):  # O(n)
        i = len(lst) // 2
        self.cur_size = len(lst)
        self.heap_list = [0] + lst
        while i > 0:
            self.perc_down(i)
            i -= 1


# 堆排序 O(n log n)
# pass
# 二叉查找树
# put, get, del, len, in
# BST:
# 比父节点小的都出现在左子树，大的都出现在右子树
class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, cur_node):
        if key < cur_node.key:
            if cur_node.hasLeftChild():
                self._put(key, val, cur_node.leftChild)
            else:
                cur_node.leftChild = TreeNode(key, val, parent=cur_node)
        else:
            if cur_node.hasRightChild():
                self._put(key, val, cur_node.rightChild)
            else:
                cur_node.rightChild = TreeNode(key, val, parent=cur_node)

    def __setitem__(self, k, v):
        self.put(k, v)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, cur_node):
        if not cur_node:
            return None
        elif cur_node.key == key:
            return cur_node
        elif key < cur_node.key:
            return self._get(key, cur_node.leftChild)
        else:
            return self._get(key, cur_node.rightChild)

    def __getitem__(self, key):
        res = self.get(key)
        if res:
            return res
        else:
            raise KeyError('Error, key not in tree')

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    @staticmethod
    def remove(cur_node):
        if cur_node.isLeaf():  # leaf
            if cur_node == cur_node.parent.leftChild:
                cur_node.parent.leftChild = None
            else:
                cur_node.parent.rightChild = None
        elif cur_node.hasBothChildren():  # interior
            succ = cur_node.find_successor()
            succ.spliceOut()
            cur_node.key = succ.key
            cur_node.payload = succ.payload
        else:  # this node has one child
            if cur_node.hasLeftChild():
                if cur_node.isLeftChild():
                    cur_node.leftChild.parent = cur_node.parent
                    cur_node.parent.leftChild = cur_node.leftChild
                elif cur_node.isRightChild():
                    cur_node.leftChild.parent = cur_node.parent
                    cur_node.parent.rightChild = cur_node.leftChild
                else:
                    cur_node.replaceNodeData(cur_node.leftChild.key,
                                             cur_node.leftChild.payload,
                                             cur_node.leftChild.leftChild,
                                             cur_node.leftChild.rightChild)
            else:
                if cur_node.isLeftChild():
                    cur_node.rightChild.parent = cur_node.parent
                    cur_node.parent.leftChild = cur_node.rightChild
                elif cur_node.isRightChild():
                    cur_node.rightChild.parent = cur_node.parent
                    cur_node.parent.rightChild = cur_node.rightChild
                else:
                    cur_node.replaceNodeData(cur_node.rightChild.key,
                                             cur_node.rightChild.payload,
                                             cur_node.rightChild.leftChild,
                                             cur_node.rightChild.rightChild)

    def inorder(self):
        self._inorder(self.root)

    def _inorder(self, tree):
        if tree is not None:
            self._inorder(tree.leftChild)
            print(tree.key)
            self._inorder(tree.rightChild)

    def postorder(self):
        self._postorder(self.root)

    def _postorder(self, tree):
        if tree:
            self._postorder(tree.rightChild)
            self._postorder(tree.leftChild)
            print(tree.key)

    def preorder(self):
        self._preorder(self.root)

    def _preorder(self, tree):
        if tree:
            print(tree.key)
            self._preorder(tree.leftChild)
            self._preorder(tree.rightChild)


class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = 0

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def find_successor(self):
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.find_successor()
                    self.parent.rightChild = self
        return succ

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def __iter__(self):
        """The standard inorder traversal of a binary tree."""
        if self:
            if self.hasLeftChild():
                for elem in self.leftChild:
                    yield elem
            yield self.key
            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem


# AVL 树
# AVL ADT Map
class AVLTree(BinarySearchTree):
    def _put(self, key, val, cur_node):
        if key < cur_node.key:
            if cur_node.hasLeftChild():
                self._put(key, val, cur_node.leftChild)
            else:
                cur_node.leftChild = TreeNode(key, val, parent=cur_node)
                self.updateBalance(cur_node.leftChild)
        else:
            if cur_node.hasRightChild():
                self._put(key, val, cur_node.rightChild)
            else:
                cur_node.rightChild = TreeNode(key, val, parent=cur_node)
                self.updateBalance(cur_node.rightChild)

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent is not None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                # Do an LR Rotation
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                # single left
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                # Do an RL Rotation
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                # single right
                self.rotateRight(node)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild is not None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild is not None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)


if __name__ == "__main__":
    pass

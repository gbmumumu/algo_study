#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random


# 线性结构是一种有序数据项的集合，其中每个数据项都有唯一的前驱与后继
# "左、右"/端 "前， 后"/端 "顶，底"/端
# 不同的线性结构的关键区别在于数据项的增减的方式
# >>>>  栈，队列，双端队列，列表 <<<<

# stack: top-base
# Last in first out -> LIFO
# Empty stack; Push; Pop; Peek; Size

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        # self.items.insert(0, item)

    def pop(self):
        return self.items.pop()
        # self.items.pop(0)

    def peek(self):
        return self.items[-1]
        # return self.items[0]

    def is_empty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def travel(self):
        for item in self.items:
            print(item, end=' ')


# app
# 括号匹配
# (开括号 )闭括号
# 对括号是否正确匹配的识别，是很多语言编译器的基础算法

def quote_matcher(symbol_string):
    s = Stack()
    balanced = True
    index = 0
    while index < len(symbol_string) and balanced:
        symbol = symbol_string[index]
        # if symbol in '([{':
        if symbol == '(':
            s.push(symbol)
        else:
            if s.is_empty():
                balanced = False
            else:
                s.pop()
                # top = s.pop()
                # def matches(open, close):
                #     opens = '([{'
                #     closes = ')]}'
                #     return opens.index(open) == closes.index(close)
                # if not matches(top, symbol):
                #     balanced = False
        index += 1
    if balanced and s.is_empty():
        return True
    return False


print(quote_matcher('((()))'))


# app
# 进制转换
# i x 进制 ** n 次方
# (233)10  = 2 x 10 **2 + 3 x 10 ** 1 + 3 x 10 ** 0
# (11101001)2 = 1 x 2 **7 + 1 x2 **6 + ... + 1 x 2 **0
# 10-> 2 除以2求余数
# (233)10 = (351)8 和 (E9)16 E=14

def user_bin(n, base):
    digits = "0123456789ABCDEF"
    s = Stack()
    while n > 0:
        rem = n % base  # 其他转换改变为除以n求余数
        s.push(rem)
        n //= base
    bin_string = ''

    while not s.is_empty():
        bin_string += digits[s.pop()]

    return bin_string


print(user_bin(25, 2))
print(user_bin(25, 16))


# app
# 中缀表达式转换与求值
# 全括号中缀表达式
# 移动操作符-> 前缀/后缀
# method 1: 先转换为全括号，再讲操作符移动到 左括号/右括号 即可得到对应的前/后缀表达式
# method 2: 用栈来保存暂时未处理的操作符； 栈顶的操作符就是最近暂存进去的，
#           当遇到新的操作符时，就需要比较优先级，再决定

def trans_expr(token: str):
    op_stack = Stack()
    token_lst = token.split()
    tail_expr = []
    prior = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 1}
    for tk in token_lst:
        if tk.isalpha() or tk.isdigit():
            tail_expr.append(tk)
        elif tk == '(':
            op_stack.push(tk)
        elif tk == ')':
            top_tk = op_stack.pop()
            while top_tk != '(':
                tail_expr.append(top_tk)
                top_tk = op_stack.pop()
        else:
            while (not op_stack.is_empty()) and (prior[op_stack.peek()] >= prior[tk]):
                tail_expr.append(op_stack.pop())
            op_stack.push(tk)
    while not op_stack.is_empty():
        tail_expr.append(op_stack.pop())

    return " ".join(tail_expr)


print(trans_expr('A + B * C'))


def calc_sfx_expr(token: str):
    token_lst = token.split()
    operand_stack = Stack()
    for tk in token_lst:
        if tk.isdigit():
            operand_stack.push(tk)
        else:
            operand_a = operand_stack.pop()
            operand_b = operand_stack.pop()
            results = eval(f'{operand_b}{tk}{operand_a}')
            operand_stack.push(results)

    return operand_stack.pop()


print(calc_sfx_expr('4 5 6 * +'))


# 队列
# 新数据项的添加总发生在一端（通常称为尾端 rear）移除在另一端（通常称为 front）
# First in first out (FIFO)
# 仅有一个入口和出口
# 有次序的数据集合
# enqueue, dequeue, is_empty, size

class Queue:
    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)
        # self.items.append(item)

    def dequeue(self):
        return self.items.pop()
        # return self.items.pop(0)


# app
# 热土豆
def deliver_potato(name_lst, num):
    sim_queue = Queue()
    for name in name_lst:
        sim_queue.enqueue(name)

    while sim_queue.size() > 1:
        for _ in range(num):
            sim_queue.enqueue(sim_queue.dequeue())
        sim_queue.dequeue()

    return sim_queue.dequeue()


print(deliver_potato(['Bill', 'David', 'Susan', 'Jane', 'Kent', 'Brad'], 7))


# app
# 打印任务
# 按照概率生成打印作业，加入打印队列
# 如果打印机空闲且队列不为空，则取出队首作业打印，记录此作业的打印时间
# 如果打印机忙，则按照打印速度进行1秒打印
# 如果当前作业打印完成，则打印机进入空闲

class PrintMachine:
    def __init__(self, ppm):
        self.page_rate = ppm  # 打印速度
        self.current_task = None  # 打印任务
        self.time_remaining = 0  # 任务倒计时

    def tick(self):
        if self.current_task is not None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_task = None

    def is_busy(self):
        return self.current_task is not None

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate


class Task:
    def __init__(self, time):
        self.time_stamp = time
        self.pages = random.randint(1, 21)

    def get_stamp(self):
        return self.time_stamp

    def get_pages(self):
        return self.pages

    def wait_time(self, current_time):
        return current_time - self.time_stamp

    @staticmethod
    def new_print_task():
        num = random.randrange(1, 181)
        return num == 180


def simulation(num_seconds, pages_per_minute):
    lab_printer = PrintMachine(pages_per_minute)
    print_queue = Queue()
    waiting_time = []

    for current_second in range(num_seconds):
        if Task.new_print_task():
            task = Task(current_second)
            print_queue.enqueue(task)

        if not lab_printer.is_busy() and not print_queue.is_empty():
            next_task = print_queue.dequeue()
            waiting_time.append(current_second)
            lab_printer.start_next(next_task)
        lab_printer.tick()

    average_wait_time = sum(waiting_time) / len(waiting_time)
    print("Average wait %6.2f secs %3d tasks remaining" \
          % (average_wait_time, print_queue.size()))


for _ in range(10):
    simulation(3600, 5)


# 双端队列 deque
# 继承了栈和队列的能力
# 不具有LIFO/LIFO
# 需要使用着自己来自行为何操作的一致性
# add_front, add_rear, remove_front, remove_rear

class Deque:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def add_rear(self, item):
        self.items.insert(0, item)

    def rm_rear(self):
        return self.items.pop(0)

    def add_front(self, item):
        self.items.append(item)

    def rm_front(self):
        return self.items.pop()


# 回文词的判定
# "radar", "madam", "toot"

def pal_checker(string):
    char_deque = Deque()
    for char in string:
        char_deque.add_rear(char)

    still_equal = True
    while char_deque.size() > 1 and still_equal:
        first = char_deque.rm_front()
        last = char_deque.rm_rear()
        if first != last:
            still_equal = False

    return still_equal


print(pal_checker('madam'))
print(pal_checker('earth'))


# unsorted list
# 无序表
# add, remove, search, is_empty, size, append, index, insert, pop
# 采用链表实现无序表

class Node:
    def __init__(self, init_dat):
        self.dat = init_dat
        self.next = None

    def get_dat(self):
        return self.dat

    def get_next(self):
        return self.next

    def set_dat(self, new_dat):
        self.dat = new_dat

    def set_next(self, new_next):
        self.next = new_next


class UnsortedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def add(self, item):
        tmp = Node(item)
        tmp.set_next(self.head)
        self.head = tmp

    def size(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next

        return count

    def search(self, item):
        cur = self.head
        found = False
        while cur is not None and not found:
            if cur.get_dat() == item:
                found = True
            else:
                cur = cur.next

        return found

    def remove(self, item):
        cur = self.head
        previous = None
        found = False
        while not found:
            if cur.get_dat() == item:
                found = True
            else:
                previous = cur
                cur = cur.next
        if previous is None:
            self.head = cur.next
        else:
            previous.set_next(cur.next)

    def append(self, item):
        tmp = Node(item)
        cur = self.head
        while cur is not None:
            cur = cur.next
        cur.set_next(tmp)

    def pop(self, index):
        pass


# 有序表
# OrderedList
# 以链表形式
# is_empty, size, remove

class OrderedList:
    def __init__(self):
        self.head = None

    def search(self, item):
        cur = self.head
        found = False
        stop = False

        while cur is not None and not found and not stop:
            if cur.get_dat() == item:
                found = True
            else:
                if cur.get_dat() > item:
                    stop = True
                else:
                    cur = cur.next

        return found

    def add(self, item):
        cur = self.head
        previous = None
        stop = False
        while cur is not None and not stop:
            if cur.get_dat() > item:
                stop = True
            else:
                previous = cur
                cur = cur.next
        tmp = Node(item)
        if previous is None:
            tmp.set_next(self.head)
            self.head = tmp
        else:
            tmp.set_next(cur)
            previous.set_next(tmp)

    def is_empty(self):
        return self.head is None

    def size(self):
        cur = self.head
        count = 0
        while cur is not None:
            count += 1
            cur = cur.next

        return count


if __name__ == "__main__":
    pass

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

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



if __name__ == "__main__":
    pass

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from time import time


# 基于有穷观点的能行方法

def gcd(m, n):
    r = m % n
    while r != 0:
        m, n = n, r
        r = m % n

    return n


# 变位词
def find_anagram(wa, wb):
    def solution_1(sa, sb):
        for i in sa:
            if i not in sb:
                return False
        return True

    def solution_2(sa, sb):
        sal = list(sa)
        sbl = list(sb)
        sal.sort()
        sbl.sort()
        if sal != sbl:
            return False
        return True

    def solution_3(sa, sb):
        c1, c2 = [0, ] * 26, [0, ] * 26
        for i, char_a in enumerate(sa):
            pos = ord(char_a) - ord('a')
            c1[pos] = c1[pos] + 1
        for j, char_b in enumerate(sb):
            pos = ord(char_b) - ord('a')
            c2[pos] = c2[pos] + 1

        count = 0
        still_ok = True
        while count < 26 and still_ok:
            if c1[count] != c2[count]:
                still_ok = False
                break
            count += 1

        return still_ok

    for i in range(1, 4):
        t1 = time()
        res = eval('solution_{}(wa, wb)'.format(i))
        t2 = time()
        dt = t2 - t1
        print(res, dt)


# list 方法比较

def test_list():
    def m0():
        l = []
        for i in range(1000):
            l = l + [i]

    def m1():
        l = []
        for i in range(1000):
            l.append(i)

    def m2():
        l = [i for i in range(1000)]

    def m3():  # fastest!
        l = list(range(1000))

    for i in range(4):
        t1 = time()
        eval(f'm{i}()')
        t2 = time()
        print(i, t2 - t1)

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
一个字符串中找出连续最长的数字串

返回最后一个最长的
0-9， +， -， .

1234567890abcd9.+12345.678.9ed
+123456.678
"""


def find_ml_num(strings: str):
    dp = [0] * len(strings)
    max_count = 0
    have_point = False
    count_point = 0
    dp[0] = 1 if strings[0].isdigit() else 0
    for cur in range(1, len(strings)):
        present_char, last_char = strings[cur], strings[cur - 1]
        if present_char == '+' or present_char == '-':
            dp[cur] = 1
            have_point = False
        elif present_char.isalpha():
            dp[cur] = 0
            have_point = False
        elif present_char.isdigit():
            if dp[cur - 1]:
                dp[cur] = dp[cur - 1] + 1
            else:
                dp[cur] = 1
        elif present_char == '.':
            if dp[cur - 1]:
                if last_char.isdigit():
                    if not have_point:
                        dp[cur] = dp[cur - 1] + 1
                        have_point = True
                    # else:
                    #    dp[cur] = 0
                    #    have_point = False
                # else:
                #    dp[cur] = 0
                #    have_point = False
            # else:
            #    dp[cur] = 0
            #    have_point = False
            if not have_point:
                dp[cur] = 0
        else:
            raise ValueError

        if dp[cur] >= max_count:
            max_count = dp[cur]
            count_point = cur

    return strings[count_point - max_count + 1:count_point + 1]


test = "1234567890abcd9.+12345.678.9ed"
res = find_ml_num(test)
# print(res)

"""
任务调度
处理器的个数m
作业数n
每个作业的处理时间tn

1. 并行
2. 最短优先
3. 当n>m时，处理最短的作业，
4. 求所有作业处理完的耗时
5. 输入： 
6. m:3 ,n:5 8 4 3 1 10
13, 
"""
# 优先队列
processor = 3
jobs = 5
jobs_time = [8, 4, 3, 1, 10]


def find_min_time(m, n, cost):
    class BinaryHeap:
        def __init__(self):
            self.heap_lst = [0]
            self.cur_size = 0

        def upward(self, i):
            while i // 2 > 0:
                if self.heap_lst[i] < self.heap_lst[i // 2]:
                    tmp = self.heap_lst[i // 2]
                    self.heap_lst[i // 2] = self.heap_lst[i]
                    self.heap_lst[i] = tmp
                i //= 2

        def find_min_child(self, i):
            if 2 * i + 1 > self.cur_size:
                return i * 2
            else:
                if self.heap_lst[i * 2] < self.heap_lst[i * 2 + 1]:
                    return i * 2
                else:
                    return i * 2 + 1

        def downward(self, i):
            while i * 2 <= self.cur_size:
                mc = self.find_min_child(i)
                if self.heap_lst[i] > mc:
                    tmp = self.heap_lst[i]
                    self.heap_lst[i] = self.heap_lst[mc]
                    self.heap_lst[mc] = tmp
                i = mc

        def insert(self, k):
            self.heap_lst.append(k)
            self.cur_size += 1
            self.upward(self.cur_size)

        def pop_min(self):
            try:
                val = self.heap_lst[1]
            except IndexError:
                return None
            else:
                self.heap_lst[1] = self.heap_lst[self.cur_size]
                self.cur_size -= 1
                self.heap_lst.pop()
                self.downward(1)
            return val

        def is_empty(self):
            return self.cur_size == 0

    if n < m:
        return max(cost)
    else:
        heap = BinaryHeap()
        for x in cost:
            heap.insert(x)
        cpus = [[0] * 2 for _ in range(m)]
        complete = False
        cpu_time = 0
        while not complete:
            if n > 0:
                for i in range(m):
                    if cpus[i][0] == 0:
                        cpus[i][0] = 1
                        job = heap.pop_min()
                        if job is None:
                            job = 0
                            cpus[i][0] = 0
                        cpus[i][1] = job
                n -= 1
            idle_cpus = 0
            for k in range(m):
                if cpus[k][1] > 0:
                    cpus[k][1] = cpus[k][1] - 1
                if cpus[k][1] == 0:
                    cpus[k][0] = 0
            cpu_time += 1
            for j in range(m):
                if not cpus[j][0]:
                    idle_cpus += 1
            if idle_cpus == m:
                complete = True

        return cpu_time


result = find_min_time(processor, jobs, jobs_time)
# print(result)

"""
MN 数组， Mi 第I个水果的成本价，Ni售价，本钱K，求这个人最多能赚多少钱

买一次，卖一次

M,N <= 50
数组元素是正整数，不超过1000；

M： 4， 2， 6， 4
N： 5， 3， 8， 7
K ： 15
输出 22
"""
m = [4, 2, 6, 4]
n = [5, 3, 8, 7]
k = 15


def get_max_profit(cost_prices, selling_prices, money):
    goods = len(cost_prices)
    visited = [False] * goods
    profit = [(selling_prices[i] - cost_prices[i]) / cost_prices[i]
              for i in range(goods)]
    lbs = [i for i in range(goods)]
    goods_info = dict(zip(lbs, sorted(list(zip(cost_prices, selling_prices, profit)),
                                      key=lambda x: x[-1], reverse=True)))
    # print(goods_info)
    pr = -1
    prs = []
    while not all(visited):
        i = 0
        while i < goods:
            if not visited[i] and goods_info[i][0] < money:
                money -= goods_info[i][0]
                visited[i] = True
                prs.append(goods_info[i][1])
            i += 1
        money += sum(prs)
        prs.clear()
        if money == pr:
            break
        pr = money
    # print(pr)
    return pr


max_profit = get_max_profit(m, n, k)
# print(max_profit)

"""
连续输入字符串
字符串个数N
N个字符串， len <=100， 空格分隔
按照长度为8拆分每个字符串，再输入到新的数组中，升序排列

输入：2 ，abc 123456789 
输出： 12345678 90000000 abc00000
"""

n = 2
input_string = "abc 123456789"


def sort(string):
    results = []

    def add_zero(strs):

        length = len(strs)
        if length == 8:
            results.append(strs)
            return strs
        if length < 8:
            strs += '0' * (8 - length)
            results.append(strs)
            return strs
        else:
            results.append(strs[:8])
            return add_zero(strs[8:])

    string_lst = string.split()
    for item in string_lst:
        add_zero(item)
    results.sort()
    return results


sorted_string = sort(input_string)

"""

独木桥

跳青蛙， 避开石子， 0…1…L L桥的长度， 以此跳跃 [S,T] 跳到L时， 
独木桥的长度， S,T，石子的位置，让青蛙过河并

L>=1 <=10^9
1<=S <= T<=10, 1<=M(石子个数)<=100
M个正整数表示桥上石子的位置，桥的起点和终点没石子

L = 10

2， 3， 5
2， 3， 5， 6， 7

输出： 2
"""

bridge_length = 10
jump_min = 2
jump_max = 3
number_of_stone = 5

stones = [2, 3, 5, 6, 7]


def frog_jump(bl, jump_min_val, jump_max_val, st):
    bridge = [0] * (bl + jump_max)
    dp = [-1] * (bl + jump_max)
    for i in st:
        bridge[i] = 1
    dp[0] = 0
    for i in range(jump_min_val, bl - 1 + jump_max_val + 1):
        for j in range(i - jump_max_val, i - jump_min_val + 1):
            if j >= 0 and dp[j] != -1:
                if dp[i] == -1:
                    dp[i] = dp[j] + bridge[i]
                else:
                    if dp[i] > dp[j] + bridge[i]:
                        dp[i] = dp[j] + bridge[i]

    stone_results = float('inf')

    for k in range(bl, bl - 1 + jump_max_val + 1):
        if dp[k] != -1 and dp[k] < stone_results:
            stone_results = dp[k]

    # print(stone_results)
    return stone_results


frog_jump(bridge_length, jump_min, jump_max, stones)

"""
股票

买入，卖出 获得最大收益

输入一个大小为n的数组， price= [p1, p2, pN]
第i天的股票价格
股票价格+ Y/S RMB/DOLLER
1DOLLER = 7 RMB

123Y
123S
假设在任何一天买入或卖出或放弃，交易周期N天内能获得的最大收益，RMB
输入： 2Y 3S 4S 6Y 3S 
76 RMB
"""

stock = ['2Y', '3S', '4S', '6Y', '3S']


def get_stock_max_profit(stocks):
    prices = []
    if len(stocks) == 1:
        return 0

    for i in stocks:
        if i.endswith('Y'):
            prices.append(int(i[0]))
        else:
            prices.append(int(i[0]) * 7)

    length = len(prices)
    start_price = [0] * length
    end_price = [0] * length
    min_price = prices[0]
    for i in range(length):
        start_price[i] = max([start_price[i - 1], prices[i] - min_price])
        min_price = min([prices[i], min_price])
    max_price = prices[-1]

    for i in range(length - 2, 0, -1):
        end_price[i] = max([end_price[i + 1], max_price - prices[i]])
        max_price = max([max_price, prices[i]])

    max_earn = 0
    for i in range(length):
        max_earn = max([start_price[i] + end_price[i], max_earn])
    #print(max_earn)  # 41
    # return max_earn

    min_price = prices[0]
    max_earn = 0
    for i in range(length):
        if prices[i] - min_price > max_earn:
            max_earn = prices[i] - min_price
        if min_price > prices[i]:
            min_price = prices[i]
    #print(max_earn)  # 26
    # return max_earn

    sum_earn = 0
    for i in range(1, length):
        if prices[i - 1] < prices[i]:
            sum_earn += prices[i] - prices[i - 1]

    #print(sum_earn)  # 41
    # return sum_earn

    k = length
    l = [[0] * (k + 1) for _ in range(length)]
    g = [[0] * (k + 1) for _ in range(length)]
    for i in range(1, length):
        diff = prices[i] - prices[i - 1]
        for j in range(1, k + 1):
            l[i][j] = max(g[i - 1][j - 1] + max(diff, 0), l[i - 1][j] + diff)
            g[i][j] = max(g[i - 1][j], l[i][j])

    # print(g[length - 1][k])
    return g[length - 1][k]


get_stock_max_profit(stock)

"""
N颗树，第I个树上有i个桃子， h小时回来， 吃桃速度为k个/每小时，可以选择一个树上吃k个， 
小于k则全吃， 在h小时内的速度k

输入： 3 11 6 7 ，8（h）
输出： 4
"""
apple = [3, 11, 6, 7]
hour = 8


def calc_speed(trees, h):
    trees.sort()
    min_k = trees[0]
    max_k = trees[-1]

    def floor(num, base):
        if num <= base:
            return 1
        else:
            return num // base + floor(num % base, base)

    def judge(peach_tr, sk, max_h):
        times = 0
        num_of_peach = 0
        for i in peach_tr:
            time = floor(i, sk)
            times += time
            if times >= max_h:
                break
            num_of_peach += i
        return num_of_peach

    total_peach = sum(trees)
    still = True
    while min_k <= max_k and still:
        mid_k = (max_k + min_k) // 2
        eaten_peach = judge(trees, mid_k, h)
        if eaten_peach < total_peach:
            max_k -= 1
        else:
            if eaten_peach == total_peach:
                still = False
            min_k += 1

    # print(min_k)
    return min_k


calc_speed(apple, hour)


if __name__ == "__main__":
    print(gcd(12, 8))
    find_anagram('hello', 'helol')
    test_list()

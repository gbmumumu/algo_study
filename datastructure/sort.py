#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Bubble sort
# 对无序表进行多趟的比较交换
# 多次两两相邻比较
def bubble_sort(unsort_lst):
    for pn in range(len(unsort_lst) - 1, 0, -1):
        for i in range(pn):
            if unsort_lst[i] > unsort_lst[i + 1]:
                tmp = unsort_lst[i]
                unsort_lst[i] = unsort_lst[i + 1]
                unsort_lst[i + 1] = tmp

    return unsort_lst


lst = [54, 26, 42, 93, 17, 77, 31, 44, 55, 20]
print(bubble_sort(lst))

if __name__ == "__main__":
    pass

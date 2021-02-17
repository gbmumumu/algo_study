#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Bubble sort
# 对无序表进行多趟的比较交换
# 多次两两相邻比较 O(n^2)
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


def bubble_sort_plus(unsort_lst):
    exchanges = True
    pn = len(unsort_lst) - 1
    while pn > 0 and exchanges:
        exchanges = False
        for i in range(pn):
            if unsort_lst[i] > unsort_lst[i + 1]:
                exchanges = True
                unsort_lst[i], unsort_lst[i + 1] = unsort_lst[i + 1], unsort_lst[i]
        pn -= 1

    return unsort_lst


lst = [54, 26, 42, 93, 17, 77, 31, 44, 55, 20]
print(bubble_sort_plus(lst))


# 选择排序
def selection_sort(unsort_lst):
    for fill_slot in range(len(unsort_lst) - 1, 0, -1):
        pom = 0
        for location in range(1, fill_slot + 1):
            if unsort_lst[location] > unsort_lst[pom]:
                pom = location
        tmp = unsort_lst[fill_slot]
        unsort_lst[fill_slot] = unsort_lst[pom]
        unsort_lst[pom] = tmp

    return unsort_lst


lst = [54, 26, 42, 93, 17, 77, 31, 44, 55, 20]
print(selection_sort(lst))


# 插入排序
# insertion sort

def insertion_sort(unsort_lst):
    for index in range(1, len(unsort_lst)):
        current_val = unsort_lst[index]
        pos = index
        while pos > 0 and unsort_lst[pos - 1] > current_val:
            unsort_lst[pos] = unsort_lst[pos - 1]
            pos -= 1
        unsort_lst[pos] = current_val

    return unsort_lst


# shell 排序 O(n^3/2)
# 列表越接近有序，插入排序的比对次数就越小
# shell 排序以插入排序为基础，对无序表进行"间隔"划分子列表，每个子列表都进行插入排序

def shell_sort(unsort_lst):
    sub_lst_count = len(unsort_lst) // 2
    while sub_lst_count > 0:
        for start_pos in range(sub_lst_count):
            unsort_lst = gap_insertion_sort(unsort_lst, start_pos, sub_lst_count)

        sub_lst_count //= 2

    return unsort_lst


def gap_insertion_sort(unsort_lst, start, gap):
    for i in range(start + gap, len(unsort_lst), gap):
        cur_val = unsort_lst[i]
        pos = i
        while pos >= gap and unsort_lst[pos - gap] > cur_val:
            unsort_lst[pos] = unsort_lst[pos - gap]
            pos -= gap
        unsort_lst[pos] = cur_val
    return unsort_lst


lst = [54, 26, 42, 93, 17, 77, 31, 44, 55, 20]
print(shell_sort(lst))


# 归并排序 O(n log n)
# merge_sort
# 分治策略，递归
# 将无序表持续地分裂为两半，对两半分别进行归并排序
def merge_sort(unsort_lst):
    if len(unsort_lst) <= 1:
        return unsort_lst

    mid = len(unsort_lst) // 2
    left, right = merge_sort(unsort_lst[:mid]), merge_sort(unsort_lst[mid:])

    merged = []
    while left and right:
        if left[0] <= right[0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
    merged.extend(right if right else left)

    return merged


if __name__ == "__main__":
    pass

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# 顺序查找 sequential search

def sequential_search(lst, item):
    pos = 0
    found = False
    while pos < len(lst) and not found:
        if lst[pos] == item:
            found = True
        else:
            pos += 1

    return found


def ordered_sequential_search(lst, item):
    pos = 0
    found = False
    stop = False
    while pos < len(lst) and not found and not stop:
        if lst[pos] == item:
            found = True
        else:
            if lst[pos] > item:
                stop = True
            else:
                pos += 1

    return found


# 二分查找 O(log n)
def binary_search(lst, item):
    first = 0
    last = len(lst) - 1
    found = False
    while first <= last and not found:
        mid_p = (first + last) // 2
        if lst[mid_p] == item:
            found = True
        else:
            if item < lst[mid_p]:
                last = mid_p - 1
            else:
                first = mid_p + 1

    return found


def binary_search_rec(lst, item):
    if not lst:
        return False
    mid_p = len(lst) // 2
    if lst[mid_p] == item:
        return True
    else:
        if item < lst[mid_p]:
            return binary_search_rec(lst[:mid_p], item)
        else:
            return binary_search_rec(lst[mid_p + 1:], item)


if __name__ == "__main__":
    pass

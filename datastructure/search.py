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


if __name__ == "__main__":
    pass

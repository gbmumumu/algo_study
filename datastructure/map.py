#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# ADT Map
# put(key, val), get(key), del, len(), in

class HashTable:
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def hash_func(self, key):
        return key % self.size

    def re_hash(self, old_hash):
        return (old_hash + 1) % self.size

    def put(self, key, dat):
        hash_val = self.hash_func(key)
        if self.slots[hash_val] is None:
            self.slots[hash_val] = key
            self.data[hash_val] = dat
        else:
            if self.slots[hash_val] == key:
                self.data[hash_val] = dat
            else:
                next_slot = self.re_hash(hash_val)
                while self.slots[next_slot] is not None and \
                        self.slots[next_slot] != key:
                    next_slot = self.re_hash(next_slot)
                if self.slots[next_slot] is None:
                    self.slots[next_slot] = key
                    self.data[next_slot] = dat
                else:
                    self.data[next_slot] = dat

    def get(self, key):
        start_slot = self.hash_func(key)
        data = None
        stop = False
        found = False
        pos = start_slot
        while self.slots[pos] is not None and not found and not stop:
            if self.slots[pos] == key:
                found = True
                data = self.data[pos]
            else:
                pos = self.re_hash(pos)
                if pos == start_slot:
                    stop = True
        return data

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)


if __name__ == "__main__":
    pass

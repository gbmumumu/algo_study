#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# simple example:
def recursion_sum(lst):
    if len(lst) == 1:
        return lst[0]

    return lst[0] + recursion_sum(lst[1:])


print(recursion_sum([1, 2, 3, 4, 5, 6, 7, 8]))


# 1. 基本结束条件（问题最小规模的直接解决）
# 2. 改变状态向基本结束条件演变（减小问题规模）
# 3. 调用自身（解决减小了规模的相同问题）

# app
# 任意进制的转换问题
def user_bin(n, base=2):
    chars = '0123456789ABCDEF'

    def _bin(num):
        if num < base:
            return chars[num]
        return _bin(num // base) + chars[num % base]

    return _bin(n)


print(user_bin(25, 16))
print(user_bin(25, 2))


# 调整深度限制
# import sys
# sys.setstructuration(3000)

# 递归可视化
# 分形树 ...
# 谢尔宾斯基三角形 ...
# 汉诺塔
def move_tower(height, from_pole, with_pole, to_pole):
    if height >= 1:
        move_tower(height - 1, from_pole, to_pole, with_pole)
        move_disk(height, from_pole, to_pole)
        move_tower(height - 1, with_pole, from_pole, to_pole)


def move_disk(disk, from_pole, to_pole):
    print(f"Moving disk {disk} from {from_pole} to {to_pole}")


move_tower(3, '#1', '#2', '#3')

# 探索迷宫

_maze_string = "0 1 0 0 0 \n" \
               "0 1 0 1 0 \n" \
               "0 0 0 0 0 \n" \
               "0 1 1 1 0 \n" \
               "0 0 0 1 0"

maze_no_wall = [[int(j) for j in i.split()] for i in _maze_string.split('\n')]
maze_no_wall.insert(0, [1] * 5)
maze_no_wall.insert(len(maze_no_wall), [1] * 5)
for i in maze_no_wall:
    i.insert(0, 1)
    i.insert(len(i), 1)

maze_1 = maze_no_wall.copy()
m, n = 5, 5
# method 1:

stack = [[1, 1, -1], ]  # (x, y, di)


def find_path(my_maze):
    global stack
    direct = [
        [0, 1],  # right
        [1, 0],  # down
        [0, -1],  # left
        [-1, 0]  # up
    ]
    my_maze[1][1] = -1
    while stack:
        tmp = stack.pop()
        _x, _y, di = tmp
        di += 1
        while di < 4:
            row = _x + direct[di][0]
            col = _y + direct[di][1]
            if my_maze[row][col] == 0:
                tmp = [_x, _y, di]
                stack.append(tmp)
                _x, _y = row, col
                my_maze[row][col] = -1
                if _x == n and _y == m:
                    return True
                di = 0
            else:
                di += 1
    return False


find_path(maze_1)
# print(stack)
if stack:
    for i in stack:
        x, y, _ = i
        print('({},{})'.format(x - 1, y - 1))
    print('({},{})'.format(n - 1, m - 1))

# method 2:
maze_2 = maze_no_wall.copy()


def update_pos(row, col, val=-1):
    global maze_2
    maze_2[row][col] = val


def is_exit(row, col):
    if row == m and col == n:
        return True
    return False


OBSTACLE = 1
TRIED = 3
DEAD_END = 2
PART_OF_PATH = 6
PATH = []


def search(maze, start_row, start_col):
    # 从初始位置开始尝试四个方向，直到找到出路。
    # 1. 遇到障碍
    if maze[start_row][start_col] == OBSTACLE:
        return False
    # 2. 发现已经探索过的路径或死胡同
    if maze[start_row][start_col] == TRIED or \
            maze[start_row][start_col] == DEAD_END:
        return False
    # 3. 发现出口
    if is_exit(start_row, start_col):
        update_pos(start_row, start_col, PART_OF_PATH)  # 显示出口位置，注释则不显示此点
        PATH.append((start_row, start_col))
        return True
    update_pos(start_row, start_col, TRIED)  # 更新迷宫状态、设置海龟初始位置并开始尝试
    # 4. 依次尝试每个方向
    found = search(maze, start_row - 1, start_col) or \
            search(maze, start_row + 1, start_col) or \
            search(maze, start_row, start_col - 1) or \
            search(maze, start_row, start_col + 1)
    if found:  # 找到出口
        PATH.append((start_row, start_col))
        update_pos(start_row, start_col, PART_OF_PATH)  # 返回其中一条正确路径
    else:  # 4个方向均是死胡同
        update_pos(start_row, start_col, DEAD_END)
    return found


print(search(maze_2, 1, 1))


# 递归算法与分治策略
# 找零
# 贪心策略
# 每次都试图解决问题最大的一部分
# 以最多数量的最大面值硬币来迅速减少找零面值
# 然而贪心算法依赖于面值，在某些特殊的面值下会失效

def get_coin(cvl, change):  # 极其低效！
    min_coins = change
    if change in cvl:
        return 1
    else:
        for i in [c for c in cvl if c <= change]:
            num_coins = 1 + get_coin(cvl, change - i)
            if num_coins < min_coins:
                min_coins = num_coins

    return min_coins


print(get_coin([1, 5, 10, 25], 63))


# 递归方法改进
# 消除重复计算

def get_coin_faster(cvl, change, known_res):  # 记忆化/函数值缓存
    min_coins = change
    if change in cvl:
        return 1
    elif known_res[change] > 0:
        return known_res[change]
    else:
        for i in [c for c in cvl if c <= change]:
            num_coins = 1 + get_coin_faster(cvl, change - i, known_res)
            if num_coins < min_coins:
                min_coins = num_coins
                known_res[change] = min_coins
    return min_coins


print(get_coin_faster([1, 5, 10, 25], 63, [0] * 64))

# dp, 动态规划


if __name__ == "__main__":
    pass

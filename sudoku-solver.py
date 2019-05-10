#!/usr/bin/env python3
# solver.py - takes a sudoku puzzle, outputs the solution
# NOTE: cell rows and columns will be 0-indexed,
# while boxes will be 1-indexed

import random
import time
from collections import deque

import numpy as np

LINE = '|'
BOX_LINE = '||'
HLINE = '-----------------------------------------\n'
SOLUTION_STACK_SIZE = 5000

sample_board = np.array([
    [0, 0, 5, 1, 0, 3, 6, 0, 0],
    [0, 9, 7, 6, 0, 5, 0, 8, 3],
    [8, 0, 0, 0, 0, 0, 1, 2, 0],
    [0, 0, 0, 3, 9, 7, 0, 0, 2],
    [0, 0, 8, 0, 0, 0, 9, 0, 0],
    [7, 0, 0, 5, 6, 8, 0, 0, 0],
    [0, 7, 1, 0, 0, 0, 0, 0, 4],
    [4, 8, 0, 2, 0, 1, 5, 6, 0],
    [0, 0, 2, 9, 0, 4, 7, 0, 0] 
])

# boxes is indexed by cell row and col to obtain box number
boxes = np.array([
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 2, 3, 3, 3],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [4, 4, 4, 5, 5, 5, 6, 6, 6],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
    [7, 7, 7, 8, 8, 8, 9, 9, 9],
])


# box_num_to_view is a dict that maps box number to a slice of the puzzle of the box
box_num_to_view = {
    1 : np.s_[0:3, 0:3], 2 : np.s_[0:3, 3:6], 3 : np.s_[0:3, 6:9],
    4 : np.s_[3:6, 0:3], 5 : np.s_[3:6, 3:6], 6 : np.s_[3:6, 6:9],
    7 : np.s_[6:9, 0:3], 8 : np.s_[6:9, 3:6], 9 : np.s_[6:9, 6:9],
}
    

def show_board(b):
    board_view = '\n'.join([
        '-------------------------------',
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[0]),
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[1]),
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[2]),
        '-------------------------------',
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[3]),
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[4]),
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[5]),
        '-------------------------------',
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[6]),
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[7]),
        '| {}  {}  {} | {}  {}  {} | {}  {}  {} |'.format(*b[8]),
        '-------------------------------',
    ])

    board_view = board_view.replace('0', '.')
    print(board_view)


def which_box(row, col):
    '''Returns which box board[row][col] is in'''
    return boxes[row, col]


def get_box(board, box_num):
    '''Returns a view of the board corresponding to a box number'''
    return board[box_num_to_view[box_num]]


def cell_is_empty(board, row, col):
    '''Returns whether or not cell at (row, col) is empty'''
    return (board[row, col] == 0)


def move_is_valid(board, num, row, col):
    # assumes square is empty - 0 in board[row][col]
    return (
            num not in board[row, :]
        and num not in board[:, col]
        and num not in get_box(board, which_box(row, col))
    )


def board_is_full(board):
    '''Returns whether or not board is complete'''
    return np.all(board)


def next_unassigned_cell(board):
    '''Returns the row and column of next unassigned cell'''
    return np.argwhere(board == 0)[0]


def gen_possible_boards(board, row, col):
    '''Generates possible next boards, given current board and unassigned cell'''    
    next_boards = []
    for num in range(1, 10):
        if move_is_valid(board, num, row, col):
            new_board = np.copy(board)
            new_board[row, col] = num
            next_boards.append(new_board)
    
    return next_boards


def solve_backtracking(init_board):
    solution_stack = deque([init_board])

    while len(solution_stack) > 0:
        board = solution_stack.pop()
        show_board(board)

        # if board is full, then it has met all the sudoku constraints
        if board_is_full(board):
            return board
        print('\r' + '\033[1A' * 14) # used to print over previous iteration
        
        # generate next possible boards, push them onto stack
        next_row, next_col = next_unassigned_cell(board)
        next_boards = gen_possible_boards(board, next_row, next_col)

        for b in next_boards:
            solution_stack.append(b)
    
    return None


def parse_from_string(s):
    '''Returns a sudoku matrix from a 81-character string, with 0s as empty cells'''
    board = np.zeros(81, dtype=np.uint8)
    for i in range(len(board)):
        board[i] = int(s[i]) if s[i].isdigit() else 0
    board = board.reshape(9, 9)
    return board

      
def main():
    with open('puzzles.sdm', 'r') as f:
        lines = f.readlines()
    
    print('Sudoku Solver')
    print('This script solves sudoku puzzles using a stack-based backtracking algorithm.')
    
    random_puzzle = parse_from_string(random.choice(lines))
    print('Given puzzle:')
    show_board(random_puzzle)    

    print()
    print('Solution:')
    solution = solve_backtracking(random_puzzle)
    
    if solution is None:
        print('No solution!')


if __name__ == '__main__':
    main()

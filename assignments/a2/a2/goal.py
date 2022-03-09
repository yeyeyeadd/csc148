"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement Me
    colour = COLOUR_LIST[:]
    a = random.randint(0, 1)
    lst = []
    for _ in range(num_goals):
        col = random.choice(colour)
        if a == 0:
            lst.append(PerimeterGoal(col))
        else:
            lst.append(BlobGoal(col))
        colour.remove(col)
    return lst


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    size = pow(2, (block.max_depth - block.level))
    half = size // 2
    if len(block.children) == 0:
        lst = []
        for _ in range(size):
            col = []
            for _ in range(size):
                col.append(block.colour)
            lst.append(col)
        return lst

    r0, r1 = _flatten(block.children[0]), _flatten(block.children[1])
    r2, r3 = _flatten(block.children[2]), _flatten(block.children[3])
    lst = _help_flatten(size)
    for i in range(size):
        for j in range(size):
            if (i < half) and (j < half):
                lst[i][j] = r1[i][j]
            elif i < half <= j:
                lst[i][j] = r2[i][j - half]
            elif j < half <= i:
                lst[i][j] = r0[i - half][j]
            else:
                lst[i][j] = r3[i - half][j - half]
    return lst


def _help_flatten(size: int) -> List[List[int]]:
    """Returns a <size> by <size> matrix whose entries are all 0.

    >>>_help_flatten(2)
    [[-1, -1], [-1, -1]]
    """
    lst = []
    for i in range(size):
        lst.append([])
        for _ in range(size):
            lst[i].append(-1)
    return lst


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    === Precondition ===
    colour should in the COLOUR_LIST
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """Perimeter Goal
     calculate the score base on edge"""
    def score(self, board: Block) -> int:
        """Return a int, by calculate the score for the board. your score will
        base on the many of unit cell on the edge, each get 1 mark. (on the
        corner will get 2)"""
        new_board = _flatten(board)
        score = 0
        for r in range(len(new_board)):
            if new_board[r][0] == self.colour:
                score += 1
            if new_board[0][r] == self.colour:
                score += 1
            if new_board[len(new_board) - 1][r] == self.colour:
                score += 1
            if new_board[r][len(new_board) - 1] == self.colour:
                score += 1
        return score

    def description(self) -> str:
        """Return a string, that descried what your goal. """
        return "Your goal is to have block on the edge with colour\
        {name}".format(name=colour_name(self.colour))


class BlobGoal(Goal):
    """Blod Goal
    calculate the score base on the largest area"""
    def score(self, board: Block) -> int:
        """Return a int, by calculate the score for the board. your score will
        base on the largest area that you have with your goal of colour"""
        score = 0
        new_board = _flatten(board)
        visit_board = _help_flatten(len(new_board))

        for c in range(len(new_board)):
            for r in range(len(new_board)):
                score = max(score,
                            self._undiscovered_blob_size((c, r), new_board,
                                                         visit_board))
        return score

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        out_of_bounds = False
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= len(board[0]) or \
                pos[1] >= len(board[0]):
            out_of_bounds = True
        if out_of_bounds or visited[pos[0]][pos[1]] != -1:
            return 0
        elif board[pos[0]][pos[1]] != self.colour:
            visited[pos[0]][pos[1]] = 0
            return 0
        else:
            visited[pos[0]][pos[1]] = 1
            n, s = self._undiscovered_blob_size((pos[0], pos[1] + 1), board,
                                                visited), \
                   self._undiscovered_blob_size((pos[0], pos[1] - 1), board,
                                                visited)
            w, e = self._undiscovered_blob_size((pos[0] - 1, pos[1]), board,
                                                visited), \
                   self._undiscovered_blob_size((pos[0] + 1, pos[1]), board,
                                                visited)
            total = n + s + e + w
            return 1 + total

    def description(self) -> str:
        """Return a string, that descried what your goal."""
        return "Your goal is to have as large as possible area content each\
        other with colour{name} (sides touch only)".format\
            (name=colour_name(self.colour))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })

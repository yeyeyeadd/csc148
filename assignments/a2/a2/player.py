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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    # TODO: Implement Me
    goal = generate_goals(num_human + num_random + len(smart_players))
    lst = []
    for i in range(len(goal)):
        if i < num_human:
            lst.append(HumanPlayer(i, goal[i]))
        elif i - num_human < num_random:
            lst.append(RandomPlayer(i, goal[i]))
        else:
            a = 0
            lst.append(SmartPlayer(i, goal[i], smart_players[a]))
            a += 1
    return lst


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    # TODO: Implement me
    loc = (block.position[0] + block.size - 1, block.position[1] + \
           block.size - 1)
    if level == 0 and block.position[0] <= location[0] <= loc[0] and \
            block.position[1] <= location[1] \
            <= loc[1]:
        return block
    if len(block.children) == 0 and block.level <= level and block.position[0] \
            <= location[0] <= loc[0] and block.position[1] <= location[1] \
            <= loc[1]:
        return block
    elif len(block.children) == 4:
        lst = []
        for child in block.children:
            if child.level <= level and child.position[0] \
                    <= location[0] <= child.position[0] + child.size - 1 \
                    and child.position[1] <= location[1] <= child.position[1] \
                    + child.size - 1:
                lst.append(child)
            if _get_block(child, location, level) is not None:
                lst.append(_get_block(child, location, level))
        if len(lst) == 0:
            return None
        dep = lst[0]
        for i in lst:
            if dep.level < i.level:
                dep = i
        return dep
    else:
        return None


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """Random Player
    It will random choice the valid move.

    === Private Attributes ===
     _proceed:
        True when the player should make a move, False when the player should
        wait.
    """
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        n = 1
        self._proceed = False
        while n < 10:
            new_block = None
            while new_block is None:
                location = (random.randint(0, board.size),
                            random.randint(0, board.size))
                new_block = _get_block(board, location,
                                       random.randint(1, board.max_depth))
            new_board = new_block.create_copy()
            lst = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
                   SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, COMBINE, PAINT]
            a = random.choice(lst)
            if a == SWAP_HORIZONTAL and new_board.swap(0):
                return SWAP_HORIZONTAL[0], SWAP_HORIZONTAL[1], new_block
            elif a == SWAP_VERTICAL and new_board.swap(1):
                return SWAP_VERTICAL[0], SWAP_VERTICAL[1], new_block
            elif a == ROTATE_CLOCKWISE and new_board.rotate(1):
                return ROTATE_CLOCKWISE[0], ROTATE_CLOCKWISE[1], new_block
            elif a == ROTATE_COUNTER_CLOCKWISE and new_board.rotate(3):
                return ROTATE_COUNTER_CLOCKWISE[0], \
                       ROTATE_COUNTER_CLOCKWISE[1], new_block
            elif a == PAINT and new_board.paint(self.goal.colour):
                return PAINT[0], PAINT[1], new_block
            elif a == COMBINE and new_board.combine():
                return COMBINE[0], COMBINE[1], new_block
            elif a == SMASH and new_board.smashable():
                return SMASH[0], SMASH[1], new_block
            else:
                n = 1


class SmartPlayer(Player):
    """ SmartPlayer
    It will randomly try n times of move(n base on the _difficulty), and pick
    the best one.
    === Precondition ===
    _difficulty <= sum of all action
    === Private Attributes ===
    _proceed:
        True when the player should make a move, False when the player should
        wait.
    _difficulty: it is the level of the smart player, the larger the number the
    harder the difficulty.

    """
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None
        self._proceed = False
        lst = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, SWAP_HORIZONTAL, \
               SWAP_VERTICAL, SMASH, COMBINE, PAINT]
        curr_score = self.goal.score(board)
        max_score = self.goal.score(board)
        score_list = []
        i = 0
        while i < self._difficulty:
            new_b = board.create_copy()
            new_block = None
            new_board = None
            while new_block is None:
                location = (random.randint(0, board.size - 1),
                            random.randint(0, board.size - 1))
                new_block = _get_block(board, location,
                                       random.randint(0, board.max_depth))
                new_board = _get_block(new_b, location,
                                       random.randint(0, board.max_depth))
            a = random.choice(lst)
            if a == SWAP_HORIZONTAL:
                if new_board.swap(0):
                    i += 1
                    score_list.append((self.goal.score(new_b),
                                       SWAP_HORIZONTAL, new_block))
            elif a == SWAP_VERTICAL:
                if new_board.swap(1):
                    i += 1
                    score_list.append((self.goal.score(new_b),
                                       SWAP_VERTICAL, new_block))
            elif a == ROTATE_CLOCKWISE:
                if new_board.rotate(1):
                    i += 1
                    score_list.append((self.goal.score(new_b),
                                       ROTATE_CLOCKWISE, new_block))
            elif a == ROTATE_COUNTER_CLOCKWISE:
                if new_board.rotate(3):
                    i += 1
                    score_list.append((self.goal.score(new_b),
                                       ROTATE_COUNTER_CLOCKWISE, new_block))
            elif a == PAINT:
                if new_board.paint(self.goal.colour):
                    i += 1
                    score_list.append((self.goal.score(new_b), PAINT,
                                       new_block))
            elif a == COMBINE:
                if new_board.combine():
                    i += 1
                    score_list.append((self.goal.score(new_b), COMBINE,
                                       new_block))
            elif a == SMASH:
                if new_board.smashable():
                    new_board.smash()
                    i += 1
                    score_list.append((self.goal.score(new_b), SMASH,
                                       new_block))

        for i in score_list:
            if max_score == curr_score:
                if i[0] > max_score:
                    max_score = i
            elif i[0] > max_score[0]:
                max_score = i
        if isinstance(max_score, int):
            return PASS[0], PASS[1], board
        else:
            return max_score[1][0], max_score[1][1], max_score[2]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })

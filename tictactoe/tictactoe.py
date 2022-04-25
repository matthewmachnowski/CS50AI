"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count X and O in the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize empty set of actions
    actions_set = set()

    # Iterates through the board and adds empty cells to the actions set
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value is None:
                actions_set.add((i, j))

    # Returns set of all possible actions on the board
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board) or action not in actions(board):
        raise Exception("Invalid Move.")

    # Since set is not subscriptable, storing it's values in 2 variables
    x, y = action
    board_copy = deepcopy(board)

    if board_copy[x][y] is not None:
        raise Exception("suggested action has already been taken")
    else:
        board_copy[x][y] = player(board)

    # Returns the transition state of the board
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Iterates through the rows and columns to find winning patterns
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] is not None:
            return board[i][0]
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] is not None:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[2][2] == board[1][1] is not None:
        return board[1][1]

    if board[2][0] == board[0][2] == board[1][1] is not None:
        return board[1][1]

    # If none of the conditions above are met, there are no winners.
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If someone won, returns True
    if winner(board) is not None:
        return True

    # If the board is full, returns True
    if sum(row.count(EMPTY) for row in board) == 0:
        return True

    # Else, the game is still going on
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Creating a dictionary with values for each scenario
    value = {X: 1, O: -1, None: 0}

    # Returns corresponding value from dictionary
    return value[(winner(board))]


def minvalue(board):
    """
    Returns the minimum value in a particular state.
    """
    # If game over, just return the utility of state
    if terminal(board):
        return utility(board)

    # Iterate over the available actions and return the minimum out of all maximums
    max_value = math.inf
    for action in actions(board):
        max_value = min(max_value, maxvalue(result(board, action)))

    return max_value


def maxvalue(board):
    """
    Returns the maximum value in a particular state.
    """

    if terminal(board):
        return utility(board)

    min_val = -math.inf
    for action in actions(board):
        min_val = max(min_val, minvalue(result(board, action)))

    return min_val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # If it's X player's turn. X wants to maximize the result
    if player(board) == X:
        score = -math.inf
        action_to_take = None
        # Checking MIN values for each action
        for action in actions(board):
            min_val = minvalue(result(board, action))

            if min_val > score:
                score = min_val
                action_to_take = action

        return action_to_take

    # If it's O player's turn. O wants to maximize the result
    elif player(board) == O:
        score = math.inf
        action_to_take = None
        # Checking MAX values for each action
        for action in actions(board):
            max_val = maxvalue(result(board, action))

            if max_val < score:
                score = max_val
                action_to_take = action

        return action_to_take

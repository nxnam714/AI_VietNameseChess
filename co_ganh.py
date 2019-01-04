
# ======================== Dictionary =======================================
import math
import queue

play_neighbor_list = {
    0: [1, 5, 5],
    1: [0, 2, 6],
    2: [1, 3, 6, 7, 8],
    3: [2, 4, 8],
    4: [3, 8, 9],
    5: [0, 6, 10],
    6: [0, 1, 2, 5, 7, 10, 11, 12],
    7: [2, 6, 8, 12],
    8: [2, 3, 4, 7, 9, 12, 13, 14],
    9: [4, 8, 14],
    10: [5, 6, 11, 15, 16],
    11: [6, 10, 12, 16],
    12: [6, 7, 8, 11, 13, 16, 17, 18],
    13: [8, 12, 14, 18],
    14: [8, 9, 13, 18, 19],
    15: [10, 16, 20],
    16: [10, 11, 12, 15, 17, 20, 21, 22],
    17: [12, 16, 18, 22],
    18: [12, 13, 14, 17, 19, 22, 23, 24],
    19: [14, 18, 24],
    20: [15, 16, 21],
    21: [16, 20, 22],
    22: [16, 17, 18, 21, 23],
    23: [18, 22, 24],
    24: [18, 19, 23]
}
play_turn_list = {
    0: [],
    1: [(0, 2)],
    2: [(1, 3)],
    3: [(2, 4)],
    4: [],
    5: [(0, 10)],
    6: [(0, 12), (1, 11), (2, 10), (5, 7)],
    7: [(2, 12), (6, 8)],
    8: [(2, 14), (3, 13), (4, 12), (7, 9)],
    9: [(4, 14)],
    10: [(5, 15)],
    11: [(6, 16), (10, 12)],
    12: [(6, 18), (7, 17), (8, 16), (11, 13)],
    13: [(8, 18), (12, 14)],
    14: [(9, 19)],
    15: [(10, 20)],
    16: [(10, 22), (11, 21), (12, 20), (15, 17)],
    17: [(12, 22), (16, 18)],
    18: [(12, 24), (13, 23), (14, 22), (17, 19)],
    19: [(14, 24)],
    20: [],
    21: [(20, 22)],
    22: [(21, 23)],
    23: [(22, 24)],
    24: []
}
# ======================== Common Funtion =======================================
def play_index_to_position(index):
    return divmod(index, 5)

def play_get_turned_chip(chip):
    if chip == 'b':
        return 'r'
    if chip == 'r':
        return 'b'
    return ' '

# ======================== Change state by turning =======================================
def play_let_turn(index, indexOne, indexTwo, state):
    (x, y) = play_index_to_position(index)
    #print(x, " ", y, "\n")
    (xOne, yOne) = play_index_to_position(indexOne)
    (xTwo, yTwo) = play_index_to_position(indexTwo)
    turnedChip = play_get_turned_chip(state[x][y])
    #print(turnedChip, "\n")
    if state[xOne][yOne] == turnedChip and state[xTwo][yTwo] == turnedChip:
        state[xOne][yOne] = state[x][y]
        state[xTwo][yTwo] = state[x][y]
        #print("Turn:", xOne, yOne, state[x][y])
    return
def play_change_state_by_turn(index, state):
    turnList = play_turn_list.get(index);
    for (indexOne, indexTwo) in turnList:
        play_let_turn(index, indexOne, indexTwo, state)
    return

# ======================== change state by deadEnd =======================================
def having_no_move(x, y, state):
    #print("No moves: ", x, y, "\n")
    neighbors = play_neighbor_list.get(x * 5 + y)

    for neighbor in neighbors:
        (xNei, yNei) = play_index_to_position(neighbor)
        if state[xNei][yNei] == '.':
            return False
    #print("True\n")
    return True
def play_undo_insert_to_dead_list(x, y, dead_end_list):
    undo_insert_queue = queue.Queue(maxsize=20)
    undo_insert_queue.put((x,y))
    while not undo_insert_queue.empty():
        (i, j) = undo_insert_queue.get()
        neighbors = play_neighbor_list.get(i * 5 + j)
        for neighbor in neighbors:
            (tp_i, tp_j) = play_index_to_position(neighbor)
            if (tp_i, tp_j) in dead_end_list:
                undo_insert_queue.put((tp_i, tp_j))
                dead_end_list.remove((tp_i, tp_j))
    return

def play_change_state_by_deadEnd(index, state):
    # The des position of the move
    (x, y) = play_index_to_position(index)

    turnedChip = play_get_turned_chip(state[x][y])

    # Queue of opponent chips should be check
    L = queue.Queue(maxsize=20)

    # List of chips having no moves
    dead_end_list = []

    # List of chips checked or will be checked
    cover_list = []
    cover_list.append((x, y))

    neighbors = play_neighbor_list.get(index);

    # put all neighbors of des position having no moves to queue
    for neighbor in neighbors:

        (xNei, yNei) = play_index_to_position(neighbor)
        if state[xNei][yNei] == turnedChip and having_no_move(xNei, yNei, state):
            L.put((xNei, yNei))
            cover_list.append((xNei, yNei))

    # loop until queue is empty or not dead end
    while not L.empty():
        (i, j) = L.get()
        # print(i, j)
        # check if the opponent chip is deadEnd moving
        if having_no_move(i, j, state) and (i, j) not in dead_end_list:
            #print("Dead end:", i, j)
            dead_end_list.append((i, j))
            tp_neightbors = play_neighbor_list.get(i * 5 + j)
            for tp_neightbor in tp_neightbors:
                (tp_i, tp_j) = play_index_to_position(tp_neightbor)
                if state[tp_i][tp_j] == turnedChip and (tp_i, tp_j) not in cover_list:
                    L.put((tp_i, tp_j))
                    cover_list.append((tp_i, tp_j))
        else:
            # dead_end_list.clear()
            play_undo_insert_to_dead_list(i, j, dead_end_list)

    for (i, j) in dead_end_list:
        #print("Dead end:", i, j)
        state[i][j] = state[x][y]
    return
# ======================== Merge state ==================================================
def play_merge_state(move, state, turn_state, dead_end_state):
    (x, y) = move[1]
    for i in range(5):
        for j in range(5):
            if turn_state[i][j] == state[x][y] or dead_end_state[i][j] == state[x][y]:
                state[i][j] = state[x][y]
    return
# ======================== Board copy  ==================================================

play_last_state = [
                  ['r', 'r', 'r', 'r', 'r'], \
                  ['r', '.', '.', '.', 'r'], \
                  ['b', '.', '.', '.', 'r'], \
                  ['b', '.', '.', '.', 'b'], \
                  ['b', 'b', 'b', 'b', 'b'], \
                ]
m_play_last_state = [
                  ['.', '.', 'b', '.', 'b'], \
                  ['r', 'r', '.', '.', 'b'], \
                  ['r', 'r', 'b', '.', '.'], \
                  ['r', 'r', 'b', 'b', 'b'], \
                  ['r', 'b', '.', '.', 'b'], \
                ]
def play_board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board
# ======================== Play doit: Change state ==================================================
def change_state_by_move_only(move, state):
    if move:
        new_state = play_board_copy(state)
        # pop the chessman in the source position
        (x, y) = move[0]
        # print ("x = " , x, "y = ", y, move [1])
        player = new_state[x][y]
        new_state[x][y] = '.'

        # put the chessman on the destination positon
        (x, y) = move[1]

        new_state[x][y] = player
    return new_state

def doit(move, state):
    if move:
        new_state = play_board_copy(state)
        new_state = change_state_by_move_only(move, state)
        (x, y) = move[1]
        index = x * 5 + y
        #change state of
        turn_state = play_board_copy(new_state)
        play_change_state_by_turn(index, turn_state)
        dead_end_state = play_board_copy(new_state)
        play_change_state_by_deadEnd(index, dead_end_state)

        play_merge_state(move, state, turn_state, dead_end_state)
    return turn_state
# ======================== Check wether it's a trap or not ==================================================
def play_is_traps(index, mychip, state):
    neighnors = play_neighbor_list(index)

    for neighnor in neighnors:
        (x, y) = play_index_to_position(neighnor)
        if (state[x][y] == mychip):
            move = [(x,y),play_index_to_position(index)]
            if (change_state_by_move_only(move, state) != doit(move, state)):
                return True
    return False
# ======================== the last position the chip leave ==============================================
def play_last_move(state):
    for i in range(25):
        (x, y) = play_index_to_position(i)
        if (state[x][y] == '.' and play_last_state[x][y] != '.'):
            return i
    return 25 #return 25 if it's the fisrt move
# ======================== Class Player ==================================================
class Player:
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, state):
        index = play_last_move(state)
        #print ("index ", index)
        result = [(0, 0), (0, 0)]
        if (index == 25):
            if (self.str == 'b'):
                result = [(2, 4), (1, 3)]
            else:
                result = [(2, 0), (3, 1)]
        #elif (play_is_traps(index, self.str, state)):
            #TODO
        else:
            neighnors = play_neighbor_list.get(index)
            for neighnor in neighnors:
                (x, y) = play_index_to_position(neighnor)
                if (state[x][y] == self.str):
                    result = [(x, y), play_index_to_position(index)]
        for i in range(25):
            (x, y) = play_index_to_position(i)
            if (state[x][y] == self.str):
                neighnors = play_neighbor_list.get(i)
                for neighnor in neighnors:
                    (xNei, yNei) = play_index_to_position(neighnor)
                    if (state[xNei][yNei] == '.'):
                        result = [(x, y), (xNei, yNei)]
        #play_last_state = doit(result, state)
        global play_last_state
        play_last_state = change_state_by_move_only(result, state)
        #print("result: ", result)
        return result
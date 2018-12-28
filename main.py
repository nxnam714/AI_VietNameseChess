
import imp
import time
import queue
#======================================================================


def board_print(board, move=[], num=0):

    print("====== The current board(", num, ")is (after move): ======")
    if move:
        print("move = ", move)
    for i in [4, 3, 2, 1, 0]:
        print(i, ":", end=" ")
        for j in range(5):
            print(board[i][j], end=" ")
        print()
    print("   ", 0, 1, 2, 3, 4)
    print("")


def board_copy(board):
    new_board = [[]]*5
    for i in range(5):
        new_board[i] = [] + board[i]
    return new_board

#======================================================================

def legal(move):
    return True

def get_turn_chip(chip):
    if chip == 'b':
        return 'r'
    if chip == 'r':
        return 'b'
    return ' '

def turn_chip_by_col(move, state):
    (x, y) = move[1]
    #print(get_turn_chip(state[x][y]), state[x][y - 1], state[x][y + 1])
    if state[x][y - 1] == get_turn_chip(state[x][y]) and \
            state[x][y + 1] == get_turn_chip(state[x][y]):
        state[x][y - 1] = state[x][y]
        state[x][y + 1] = state[x][y]
    return
def turn_chip_by_row(move, state):
    (x, y) = move[1]
    if state[x - 1][y] == get_turn_chip(state[x][y]) and \
            state[x + 1][y] == get_turn_chip(state[x][y]):
        state[x - 1][y] = state[x][y]
        state[x + 1][y] = state[x][y]
    return
def turn_chip_by_sec(move, state):
    (x, y) = move[1]
    if state[x - 1][y - 1] == get_turn_chip(state[x][y]) and \
            state[x + 1][y - 1] == get_turn_chip(state[x][y]):
        state[x - 1][y - 1] = state[x][y]
        state[x + 1][y - 1] = state[x][y]

    if state[x - 1][y + 1] == get_turn_chip(state[x][y]) and \
            state[x + 1][y - 1] == get_turn_chip(state[x][y]):
        state[x - 1][y + 1] = state[x][y]
        state[x + 1][y - 1] = state[x][y]
    return

def turn(move, state):
    (x, y) = move[1]
    if (x == 0 or x == 4) and (y == 0 or y == 4):
        return False
    elif x == 0 or x == 4:
        turn_chip_by_col(move, state)
        return True
    elif y == 0 or y == 4:
        turn_chip_by_row(move, state)
        return True
    elif abs(x - y) == 1:
        turn_chip_by_col(move, state)
        turn_chip_by_row(move, state)
        return
    else:
        turn_chip_by_col(move, state)
        turn_chip_by_row(move, state)
        turn_chip_by_sec(move, state)
        return

def neighbor_list(x, y):
    if x == 0 and y == 0:
        return [(0, 1), (1, 0), (1, 1)]
    if x == 0 and y == 4:
        return [(0, 3), (1, 3), (1, 4)]
    if x == 4 and y == 0:
        return [(4, 1) , (3, 0), (3, 1)]
    if (x == 1 or x == 3) and y == 0:
        return [(x - 1, y), (x + 1, y), (x, y + 1)]
    if (x == 1 or x == 3) and y == 4:
        return [(x - 1, y), (x + 1, y), (x ,y - 1)]
    if x == 0 and (y == 1 or y == 3):
        return [(x, y - 1), (x, y + 1), (x + 1, y)]
    if x == 4 and (y == 1 or y == 3):
        return [(x, y - 1), (x, y + 1), (x -1, y)]
    if (x, y) == (0, 2) or (x, y) == (4, 2):
        return [(x, 1), (x, 3), (abs(x - 1), 2), (abs(x - 1), 1), (abs(x -1), 3)]
    if (x, y) == (2, 0) or (x, y) == (2, 4):
        return [(1, y), (3, y), (1, abs(y - 1)), (3, abs(y - 1)), (2, abs(y - 1))]
    if abs(x - y) == 1:
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    else:
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x -1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
def dead_end_move (x, y, state):
    neighbors = neighbor_list(x,y)
    for (i, j) in neighbors:
        if state[i][j] == '.':
            return False
    return True

def undo_insert_to_dead_list(x, y, dead_end_list):
    undo_insert_queue = queue.Queue(maxsize=20)
    undo_insert_queue.put((x,y))
    while not undo_insert_queue.empty():
        (i, j) = undo_insert_queue.get()
        neighbors = neighbor_list(i, j)
        for (tp_i, tp_j) in neighbors:
            if (tp_i, tp_j) in dead_end_list:
                undo_insert_queue.put((tp_i, tp_j))
                dead_end_list.remove((tp_i, tp_j))
    return
def dead_end(move, state):
    #The des position of the move
    (x, y) = move[1]
    #Queue of opponent chips should be check
    L = queue.Queue(maxsize = 20)

    #List of dead end chips
    dead_end_list = []

    #List of chips checked or will be checked
    cover_list = []
    cover_list.append((x, y))

    neighbors = neighbor_list(x, y);
    #put all neighbor of des position to queue
    for (n_x, n_y) in neighbors:
        #print(n_x, n_y)
        if state[n_x][n_y] == get_turn_chip(state[x][y]) and dead_end_move(n_x, n_y, state):
            L.put((n_x, n_y))
            cover_list.append((n_x, n_y))
            #print(n_x, n_y)

    #loop until queue is empty or not dead end
    while not L.empty():
        (i, j) = L.get()
        #print(i, j)
        #check if the opponent chip is dead end moving
        if dead_end_move(i, j, state) and (i, j) in dead_end_list:
            #print("Dead end:", i, j)
            dead_end_list.append((i, j))
            tp_neightbors = neighbor_list(i , j)
            for (tp_i, tp_j) in tp_neightbors:
                if state[tp_i][tp_j] == get_turn_chip(state[x][y]) and (tp_i, tp_j) not in cover_list:
                    L.put((tp_i, tp_j))
                    cover_list.append((tp_i, tp_j))
        else:
            #dead_end_list.clear()
            undo_insert_to_dead_list(i, j, dead_end_list)
    for (i, j) in dead_end_list:
        #print("Dead end:", i, j)
        state[i][j] = get_turn_chip(state[i][j])
    return

def merge_state(move, state, turn_state, dead_end_state):
    (x, y) = move[1]
    for i in range(5):
        for j in range(5):
            if turn_state[i][j] == state[x][y] or dead_end_state[i][j] == state[x][y]:
                state[i][j] = state[x][y]
    return
#======================================================================
# Student SHOULD implement this function to change current state to new state properly
def doit(move, state):
    if legal(move) and move:
        new_state = board_copy(state)
        #pop the chessman in the source position
        (x, y) = move[0]
        #print ("x = " , x, "y = ", y, move [1])
        player = state[x][y]
        state[x][y] = '.'

        #put the chessman on the destination positon
        (x, y) = move[1]
        state[x][y] = player

        #change state of
        turn_state = board_copy(state)
        turn(move, turn_state)
        dead_end_state = board_copy(state)
        dead_end(move, dead_end_state)

        merge_state(move, state, turn_state, dead_end_state)
    return dead_end_state

#======================================================================
Initial_Board = [
                  ['b', 'r', 'r', '.', 'b'], \
                  ['b', 'b', '.', '.', '.'], \
                  ['b', 'r', 'r', '.', '.'], \
                  ['r', '.', 'r', 'r', '.'], \
                  ['b', 'r', 'b', 'b', '.'], \
                ]

# 4 : r r r r r
# 3 : r . . . r
# 2 : b . . . r
# 1 : b . . . b
# 0 : b b b b b
#     0 1 2 3 4
#======================================================================


def play(student_a, student_b, start_state=Initial_Board):
    player_a = imp.load_source(student_a, student_a + ".py")
    player_b = imp.load_source(student_b, student_b + ".py")

    a = player_a.Player('b')
    b = player_b.Player('r')
    
    curr_player = a
    state = start_state    

    board_num = 0
        
    board_print(state)
    
    while True:
        print("It is ", curr_player, "'s turn")

        start = time.time()
        move = curr_player.next_move(state)
        elapse = time.time() - start

        # print(move)

        if not move:
            break

        print("The move is : ", move, end=" ")
        print(" (in %.2f ms)" % (elapse*1000), end=" ")
        if elapse > 3.0:
            print(" ** took more than three second!!", end=" ")
            break
        print()
        # check_move
        state = doit(move, state)

        board_num += 1
        board_print(state, num=board_num)

        if curr_player == a:
            curr_player = b
        else:
            curr_player = a
        break

    print("Game Over")
    if curr_player == a:
        print("The Winner is:", student_b, 'red')
    else:
        print("The Winner is:", student_a, 'blue')

play("co_ganh", "co_ganh")

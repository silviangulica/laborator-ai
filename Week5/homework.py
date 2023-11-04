from itertools import combinations

### 1 ###

magic_square = [
    [2,7,6],
    [9,5,1],
    [4,3,8]
]
example_state = {
    "current_matrix": [[0 for _ in range(3)] for _ in range(3)],
    "current_turn": 1
}

def init_state():
    state = {
        "current_matrix": [[0 for _ in range(3)] for _ in range(3)],
        "current_turn": 1
    }
    return state

def verify_draw(state):
    for i in range(3):
        for j in range(3):
            if state['current_matrix'][i][j] == 0:
                return False
    state['current_turn'] = 0
    return True

def verify_win(state, current_turn):
    if(get_lines_count(state,current_turn) == 0  and get_columns_count(state,current_turn) == 0 and get_diagonals_count(state,current_turn) == 0):
        return False
    return True
    

def get_lines_count(state, current_player, flag=1):
    count = 0
    current_matrix = state['current_matrix']
    for i in range(3):
        if flag == 1: # flag = 1, verifica daca sunt toate egale cu current_player
            if current_matrix[i][0] == current_matrix[i][1] == current_matrix[i][2] == current_player:
                count+=1
        if flag == 2: # flag 2, verifica daca sunt egale cu 0, sau current player <- pt numarul posibil de directii
            other_player = 2 - current_player + 1
            if other_player not in current_matrix[i]:
                count+=1
    return count

def get_columns_count(state, current_player, flag=1):
    count = 0
    current_matrix = state['current_matrix']
    for j in range(3):
        if flag == 1: 
            if current_matrix[0][j] == current_matrix[1][j] == current_matrix[2][j] == current_player:
                count+=1
        if flag == 2:
            other_player = 2 - current_player + 1
            if other_player not in [current_matrix[0][j] ,current_matrix[1][j] , current_matrix[2][j]]:
                count+=1
    return count

def get_diagonals_count(state, current_player, flag=1):
    count = 0
    current_matrix = state['current_matrix']
    # verificam diagonala principala
    if flag == 1: 
        if current_matrix[0][0] == current_matrix[1][1] == current_matrix[2][2] != 0:
            count+=1
    if flag == 2: 
        other_player = 2 - current_player + 1
        if other_player not in [current_matrix[0][0], current_matrix[1][1], current_matrix[2][2]]:
            count+=1
    # verificam diagonala secundara
    if flag == 1: 
        if current_matrix[0][2] == current_matrix[1][1] == current_matrix[2][0] != 0:
            count+=1
    if flag == 2:
        other_player = 2 - current_player + 1
        if other_player not in [current_matrix[0][2], current_matrix[1][1], current_matrix[2][0]]:
            count+=1
    return count
    
### 2 ###

def transition(state, move):
    new_state = state.copy()
    
    new_state['current_matrix'] = [state["current_matrix"][i][:] for i in range(3)]
    new_state['current_matrix'][move[0]][move[1]] = state['current_turn']
    new_state['current_turn'] = 1 if state['current_turn'] == 2 else 2
    return new_state

def get_number_of_directions(state, player):
    count = 0
    count += get_lines_count(state, player, 2)
    count += get_columns_count(state, player, 2)
    count += get_diagonals_count(state, player, 2)
    return count

def choose_a_move(state,player_to_move):
    best_current_player_move = (-1,-1)
    min_number_of_directions = 999

    for i in range(3):
        for j in range(3):
            if state['current_matrix'][i][j] == 0:
                state['current_matrix'][i][j] = player_to_move
                number_of_directions = get_number_of_directions(state, 2-player_to_move+1)
                if number_of_directions < min_number_of_directions:
                    min_number_of_directions = number_of_directions
                    best_current_player_move = (i,j)
                state['current_matrix'][i][j] = 0
    return best_current_player_move

def play_ai_vs_ai():
    state = init_state()
    while True:
        if state['current_turn'] == 1:
            print("Player 1's turn")
            move = choose_a_move(state, 1)
        else:
            print("Player 2's turn")
            move = choose_a_move(state, 2)
            
        new_state = transition(state, move)
        print_matrix(state["current_matrix"]) 
        state = new_state
        if verify_win(state, 2 - state['current_turn'] + 1):
            print("Player " + str(2 - state['current_turn'] + 1) + " won!")
            break
        elif verify_draw(state):
            print("Draw!")
            break

def validate_move(state, move):
    if move[0] < 0 or move[0] > 2 or move[1] < 0 or move[1] > 2:
        return False
    if state['current_matrix'][move[0]][move[1]] != 0:
        return False
    return True


def play_player_vs_ai():
    state = init_state()
    while True:
        if state['current_turn'] == 1:
            while True:
                move = int(input("Enter the row: ")), int(input("Enter the column: "))
                if validate_move(state, move):
                    break
                else:
                    print("Invalid move!")
        else:
            print("Player 2's turn")
            move = choose_a_move(state, 2)
            
        new_state = transition(state, move)
        state = new_state
        print_matrix(state["current_matrix"]) 
        if verify_win(state, 2 - state['current_turn'] + 1):
            print("Player " + str(2 - state['current_turn'] + 1) + " won!")
            break
        elif verify_draw(state):
            print("Draw!")
            break
        
def print_matrix(matrix):
    for i in range(3):
        for j in range(3):
            print(matrix[i][j], end=" ")
        print()

#play_ai_vs_ai()


def get_possible_moves(state):
    moves = []
    for i in range(3):
        for j in range(3):
            if state['current_matrix'][i][j] == 0:
                moves.append((i,j))
    return moves


# minimizeaza Ai scorul
# maximizeaza player scorul
def minimax(depth, state, maxim):
    if verify_win(state, 1):
        return get_number_of_directions(state, 2)
    elif verify_win(state, 2):
        return -get_number_of_directions(state, 1)
    elif depth == 9:
        return 0
    
    if maxim:
        best = -1000
        for move in get_possible_moves(state):
                    new_state = transition(state, move)
                    best = max(best, minimax(depth+1, new_state, False))
        return best
    else:
        best = 1000
        for move in get_possible_moves(state):
                    new_state = transition(state, move)
                    best = min(best, minimax(depth+1, new_state, True))
        return best
    

    
def choose_a_move_minimax(state):
    best = 1000
    best_move = (-1,-1)
    for i in range(3):
        for j in range(3):
            if state['current_matrix'][i][j] == 0:
                new_state = transition(state, (i,j))
                score = minimax(0, new_state, False)
                if score < best:
                    best = score
                    best_move = (i,j)
                print("Move: ", (i,j), "Score: ", score)
     
    return best_move, best

def choose_a_move_minimax_predicted(state):
    best = -1000
    best_move = (-1,-1)
    for i in range(3):
        for j in range(3):
            if state['current_matrix'][i][j] == 0:
                new_state = transition(state, (i,j))
                score = minimax(0, new_state, True)
                if score > best:
                    best = score
                    best_move = (i,j)
                print("Move predict: ", (i,j), "Score: ", score)
     
    return best_move, best

def play_with_minimax():
    state = init_state()
    while True:
        if state['current_turn'] == 1:
            print("Player 1's turn")
            while True:
                move = int(input("Enter the row: ")), int(input("Enter the column: "))
                if validate_move(state, move):
                    break
                else:
                    print("Invalid move!")
        else:
            print("Player 2's turn")
            move, score = choose_a_move_minimax(state)
            temp_state = transition(state, move)
            pred_move, score_pred = choose_a_move_minimax_predicted(temp_state)

            print("Move: ", move, "Score: ", score)
            print("Move predict: ", pred_move, "Score: ", score_pred)
            if abs(score_pred) > abs(score):
                move = pred_move
            
        new_state = transition(state, move)
        state = new_state
        print_matrix(state["current_matrix"]) 
        if verify_win(state, 2 - state['current_turn'] + 1):
            print("Player " + str(2 - state['current_turn'] + 1) + " won!")
            break
        elif verify_draw(state):
            print("Draw!")
            break

def choose_a_move_minimax_predicted(state):
    best = -1000
    best_move = (-1,-1)
    for i in range(3):
        for j in range(3):
            if state['current_matrix'][i][j] == 0:
                new_state = transition(state, (i,j))
                score = minimax(0, new_state, True)
                if score > best:
                    best = score
                    best_move = (i,j)
                print("Move predict: ", (i,j), "Score: ", score)
     
    return best_move, best


        
play_with_minimax()
#play_player_vs_ai()
      


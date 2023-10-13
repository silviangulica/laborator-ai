### 1. Reprezentarea starii

state = {
    'matrix' : [
        [8, 6, 0],
        [5, 4, 7],
        [2, 3, 1]
    ],
    'last_moved_cell_value' : -1,
    'neighbours': {},
    'position_of_zero' : (0,2)
}

### 2. Stari speciale + functia de intializare  + functia booleana de verificare a starii finale
def init_state(vector):
    state = {}
    state['matrix'] = [vector[0:3], vector[3:6], vector[6:9]]
    state['last_moved_cell_value'] = -1
    state['neighbours'] = construct_neighbour_dict(state['matrix'])
    state['position_of_zero'] = find_position_of_zero(state['matrix'])
    return state

def construct_neighbour_dict(matrix):
    neighbour_dict = {}
    for i in range(0,3):
        for j in range(0,3):
            current_node_neighbours = []
            if i - 1 >= 0:
                current_node_neighbours.append((i-1,j))
            if i + 1 <= 2:
                current_node_neighbours.append((i+1,j))
            if j - 1 >= 0:
                current_node_neighbours.append((i,j-1))
            if j + 1 <= 2:
                current_node_neighbours.append((i,j+1))
            neighbour_dict.update({matrix[i][j]: current_node_neighbours})
    return neighbour_dict
    
def find_position_of_zero(matrix):
    for i in range(0,3):
        for j in range(0,3):
            if matrix[i][j] == 0:
                return (i,j)
    return (-1,-1)

def is_state_final(state):
    vec = state['matrix'][0] + state['matrix'][1] + state['matrix'][2]
    vec.remove(0)
    for i in range(0, len(vec) - 1):
        if(vec[i] > vec[i+1]):
            return False
    return True


### 3. Functia de tranziti

def make_one_move(state, neighbour_node_position):
    new_state = {}
    neighbour_to_be_moved = state['matrix'][neighbour_node_position[0]][neighbour_node_position[1]]
    
    print(neighbour_to_be_moved)
    print(state['last_moved_cell_value'])
    if(validate(state, neighbour_to_be_moved) == False):
        return None
    
    new_state['matrix'] = state['matrix']
    new_state['last_moved_cell_value'] = neighbour_to_be_moved
    swap_values(new_state['matrix'], state['position_of_zero'], neighbour_node_position)
    new_state['position_of_zero'] = neighbour_node_position
    new_state['neighbours'] = construct_neighbour_dict(new_state['matrix'])
    return new_state
    
    
    
def swap_values(matrix, pos1, pos2):
    matrix[pos1[0]][pos1[1]],matrix[pos2[0]][pos2[1]] = matrix[pos2[0]][pos2[1]],matrix[pos1[0]][pos1[1]]
  
    
def validate(state,neighbour_to_be_moved ):
    if(neighbour_to_be_moved == state['last_moved_cell_value']):
        return False
    return True
    
### 4. IDDFS

def iddfs(init_state, max_depth):
    for depth in range(0, max_depth):
        visited=[]
        solution = depth_limited_DFS(init_state, depth, visited)
        if solution != None:
            return solution
     
    return None

def depth_limited_DFS(state, depth, visited):
    if is_state_final(state):
        return state
    if depth == 0:
        return None
    visited.append(state)
    for neighbour_position in state['neighbours'][0]:
        neighbour_state = make_one_move(state, neighbour_position)
       
        if(neighbour_state == None):
            continue
        
        print(neighbour_state)
        print(neighbour_state['matrix'][0])
        print(neighbour_state['matrix'][1])
        print(neighbour_state['matrix'][2])
        print('----------------')
        if neighbour_state not in visited:
            result = depth_limited_DFS(neighbour_state, depth - 1, visited)
            if result != None:
                return result
    return None
          

# 0 2 1
# 3 4 5
# 6 7 8

# matrixxx=make_one_move(init_state([8, 6, 0, 5, 4, 7, 2, 3, 1]), (0,1))

print(iddfs(init_state([0, 2, 1, 3, 4, 5, 6, 7, 8]),15))
# print(matrixxx['matrix'])
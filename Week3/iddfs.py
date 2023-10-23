from icecream import ic
# 1. Reprezentarea starii

info_state = {
    "matrix": [[8, 6, 0], [5, 4, 7], [2, 3, 1]],
    "last_moved_cell_value": -1,
    "position_of_zero": (0, 2),
}


# 2. Stari speciale + functia de intializare  + functia booleana de verificare a starii finale
def init_state(vector):
    state = {"matrix": [vector[0:3], vector[3:6],
                        vector[6:9]], "last_moved_cell_value": -1}
    state["position_of_zero"] = find_position_of_zero(state["matrix"])
    return state


def construct_neighbour_of_zero_list(state):
    list_of_neighbours = []
    position_of_zero = state["position_of_zero"]
    if position_of_zero[0] > 0:
        list_of_neighbours.append(
            (position_of_zero[0] - 1, position_of_zero[1]))
    if position_of_zero[0] < 2:
        list_of_neighbours.append(
            (position_of_zero[0] + 1, position_of_zero[1]))
    if position_of_zero[1] > 0:
        list_of_neighbours.append(
            (position_of_zero[0], position_of_zero[1] - 1))
    if position_of_zero[1] < 2:
        list_of_neighbours.append(
            (position_of_zero[0], position_of_zero[1] + 1))
    return list_of_neighbours


def find_position_of_zero(matrix):
    for i in range(0, 3):
        for j in range(0, 3):
            if matrix[i][j] == 0:
                return i, j
    return -1, -1


def is_state_final(state):
    vec = state["matrix"][0] + state["matrix"][1] + state["matrix"][2]
    vec.remove(0)
    for i in range(0, len(vec) - 1):
        if vec[i] > vec[i + 1]:
            return False
    return True


# 3. Functia de tranzitii


def make_one_move(state, neighbour_node_position):
    new_state = {}
    neighbour_to_be_moved = state["matrix"][neighbour_node_position[0]][
        neighbour_node_position[1]
    ]

    if not validate(state, neighbour_to_be_moved):
        return None

    new_state["matrix"] = [row.copy() for row in state["matrix"]]
    new_state["last_moved_cell_value"] = neighbour_to_be_moved
    swap_values(new_state["matrix"],
                state["position_of_zero"], neighbour_node_position)
    new_state["position_of_zero"] = neighbour_node_position
    return new_state


def swap_values(matrix, pos1, pos2):
    matrix[pos1[0]][pos1[1]], matrix[pos2[0]][pos2[1]] = (
        matrix[pos2[0]][pos2[1]],
        matrix[pos1[0]][pos1[1]],
    )


def validate(state, neighbour_to_be_moved):
    if neighbour_to_be_moved == state["last_moved_cell_value"]:
        return False
    return True


# 4. IDDFS
def iddfs(start_state, max_depth):
    for depth in range(0, max_depth):
        visited = set()
        order_of_moves = []
        solution = depth_limited_dfs(
            start_state, depth, visited, order_of_moves)
        if solution is not None:
            return solution, order_of_moves

    return None, None


def depth_limited_dfs(state, depth, visited, order_of_moves):
    if is_state_final(state):
        order_of_moves.append(state['matrix'])
        return state
    if depth == 0:
        return None
    visited.add(str(state))
    order_of_moves.append(state['matrix'])

    for neighbour_position in construct_neighbour_of_zero_list(state):
        neighbour_state = make_one_move(state, neighbour_position)

        if neighbour_state is None:
            continue

        if str(neighbour_state) not in visited:
            result = depth_limited_dfs(
                neighbour_state, depth - 1, visited, order_of_moves)
            if result is not None:
                return result

    order_of_moves.pop()
    return None


# [8, 6, 7, 2, 5, 4, 0, 3, 1]         [2, 5, 3, 1, 0, 6, 4, 7, 8]        [2, 7 , 5, 0, 8, 4, 3, 1, 6].
ex_one_state = iddfs(init_state([8, 6, 7, 2, 5, 4, 0, 3, 1]), 30)
ic("First:" + str(ex_one_state[0]['matrix']))
for i in ex_one_state[1]:
    for j in i:
        print(j)
    print("")
#
#
# ex_two_state = iddfs(init_state([2, 5, 3, 1, 0, 6, 4, 7, 8]), 30)
# ic("Second" + str(ex_two_state['matrix']))
#
#
# ex_thr_state = iddfs(init_state([2, 7, 5, 0, 8, 4, 3, 1, 6]), 30)
# ic("Third:" + str(ex_thr_state['matrix']))

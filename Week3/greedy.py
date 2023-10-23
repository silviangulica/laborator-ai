from queue import PriorityQueue

from iddfs import is_state_final, construct_neighbour_of_zero_list
from iddfs import make_one_move

final_state = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
    0: (2, 2)
}


def calculate_manhattan(state):
    score = 0
    for i in range(3):
        for j in range(3):
            score += abs(i - final_state[state['matrix'][i][j]][0]) + \
                abs(j - final_state[state['matrix'][i][j]][1])
    return score


def check_if_final(state):
    state_vector = state['matrix'][0] + state['matrix'][1] + state['matrix'][2]

    if state_vector[7] != 0:
        return False

    for index in range(1, 9):
        if index != state_vector[index]:
            return False

    return True


def greedy(init_state, heuristic_val):
    pq = PriorityQueue()
    pq.put((init_state, heuristic_val(init_state)))
    visited = [init_state]

    while pq.empty():
        state = pq.get()

        if check_if_final(state):
            return state

        for neighbor in construct_neighbour_of_zero_list(state):
            neighbour_state = make_one_move(state, neighbor)

            if neighbour_state is None:
                continue

            pq.put((neighbor, heuristic_val(neighbor)))
            visited.append(neighbor)
    return None


print(greedy({
    'matrix': [[1, 2, 3], [8, 7, 6], [4, 5, 0]]
}, calculate_manhattan))

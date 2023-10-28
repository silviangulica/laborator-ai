from icecream import ic
import copy
import timeit

domain = {
    (0, 0): 8,
    (0, 1): 4,
    (0, 2): [i for i in range(9)],
}


def generate_domain_for_input(input_matrix):
    domain = {}
    assignment = {}
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix[i])):
            if input_matrix[i][j] == -1:  # empty grey cell
                domain[(i, j)] = [val for val in range(2, 9, 2)]
            elif input_matrix[i][j] == 0:  # empty cell
                domain[(i, j)] = [val for val in range(1, 10)]
            else:  # filled cell
                domain[(i, j)] = [input_matrix[i][j]]
            assignment[(i, j)] = input_matrix[i][j]
    return domain, assignment


matrix_input = [
    [8, 4, 0, 0, 5, 0, -1, 0, 0],
    [3, 0, 0, 6, 0, 8, 0, 4, 0],
    [0, 0, -1, 4, 0, 9, 0, 0, -1],
    [0, 2, 3, 0, -1, 0, 9, 8, 0],
    [1, 0, 0, -1, 0, -1, 0, 0, 4],
    [0, 9, 8, 0, -1, 0, 1, 6, 0],
    [-1, 0, 0, 5, 0, 3, -1, 0, 0],
    [0, 3, 0, 1, 0, 6, 0, 0, 7],
    [0, 0, -1, 0, 2, 0, 0, 1, 3],
]

def row_checker(assignment, value, current_row_index):
    for col_index in range(9):
        if (current_row_index, col_index) in assignment and assignment[(current_row_index, col_index)] == value:
            return False
    return True

def column_checker(assignment, value, current_col_index):
    for row_index in range(9):
        if (row_index, current_col_index) in assignment and assignment[(row_index, current_col_index)] == value:
            return False
    return True
def grid_checker(assignment, value, current_row_index, current_col_index):
    row_start_index = 3 * (current_row_index // 3)
    col_start_index = 3 * (current_col_index // 3)
    
    for row in range(row_start_index, row_start_index + 3):
        for col in range(col_start_index, col_start_index + 3):
            if assignment.get((row, col)) == value:
                return False
    return True
    

def is_consistent(assignment, var, value):
    i, j = var 
    if (row_checker(assignment,value,i) == False or column_checker(assignment,value,j) == False or grid_checker(assignment,value,i,j)==False):
        return False
    return True


def is_completed(domains: dict):
    for value in domains.values():
        if len(value) != 1:
            return False
    return True


def next_unassigned_variable(domain, assignment):
    for key, value in domain.items():
        if assignment[key] <= 0:
            return key
        
def next_unassigned_variable_MRV(domain, assignment):
    min = 999
    min_key = None
    for key, value in domain.items():
        if assignment[key] <= 0:
            if len(value) < min:
                min = len(value)
                min_key = key
    return min_key

def update_domains_FC(domains: dict, var: tuple, value: int):
    new_domains = copy.deepcopy(domains)

    new_domains[var].clear()
    new_domains[var].append(value)
    remove_values_from_domains(new_domains, var, value)
    return new_domains

def remove_values_from_domains(new_domains, var, value):
    i, j = var
    for row in range(9):
        if row != i:
            if value in new_domains[(row, j)]:
                new_domains[(row, j)].remove(value)
    
    for col in range(9):
        if col != j:
            if value in new_domains[(i, col)]:
                new_domains[(i, col)].remove(value)

    row_start_index = 3 * (i // 3)
    col_start_index = 3 * (j // 3)
    for row in range(row_start_index, row_start_index + 3):
        for col in range(col_start_index, col_start_index + 3):
            if row != i and col != j:
                if value in new_domains[(row, col)]:
                    new_domains[(row, col)].remove(value)

def no_empty_domains(domains):
    for key in domains:
        if len(domains[key]) == 0:
            return False
    return True


def BKT_with_FC(assignment, domains, next_unassigned_variable = next_unassigned_variable):
    if is_completed(domains):
        return assignment

    var = next_unassigned_variable(domains, assignment)  # returneaza o tupla

    for value in domains[var[0], var[1]]:
        if is_consistent(assignment, var, value):
            new_assignment = assignment.copy()
            new_assignment[(var[0], var[1])] = value

            new_domains = update_domains_FC(domains, var, value)

            if no_empty_domains(new_domains):
                res = BKT_with_FC(new_assignment, new_domains, next_unassigned_variable)
                if res is not None:
                    return res
    return None

def run_both_versions():
    domains, assignment = generate_domain_for_input(matrix_input)
    start_time = timeit.default_timer()
    assignment = BKT_with_FC(assignment, domains)
    end_time = timeit.default_timer()
    print("FC: ", end_time - start_time)
    print_assignment(assignment)
    
    domains, assignment = generate_domain_for_input(matrix_input)
    start_time = timeit.default_timer()
    assignment = BKT_with_FC(assignment, domains, next_unassigned_variable_MRV)
    end_time = timeit.default_timer()
    print("FC cu MRV: ", end_time - start_time)
    print_assignment(assignment)


def print_assignment(assignment):
    if(assignment == None):
        print("No solution")
        return
    for i in range(9):
        for j in range(9):
            print(assignment[(i, j)], end=" ")
        print()
    
    
run_both_versions()
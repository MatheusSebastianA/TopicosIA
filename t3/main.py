import sys

class CSP:
    def __init__(self):
        self.variables = {}
        self.domains = {}
        self.constraints = []

    def add_variable(self, var, domain):
        self.variables[var] = None
        self.domains[var] = domain

    def add_constraint(self, constraint_type, scope, tuples):
        self.constraints.append((constraint_type, scope, tuples))

def read_input(file_path):
    csp = CSP()
    with open(file_path, 'r') as f:
        linhas = f.readlines()

    index = 0
    num_var = int(linhas[index].strip())
    index += 1

    for i in range(num_var):
        linha = linhas[index].strip().split()
        dom_tam = int(linha[0])
        dom_valores = list(map(int, linha[1:1 + dom_tam]))
        csp.add_variable(f'x{i+1}', dom_valores)
        index += 1

    num_restricoes = int(linhas[index].strip())
    index += 1

    while index < len(linhas):
        if linhas[index].strip() in {'V', 'I'}:
            tipo_restricao = linhas[index].strip()
            index += 1

            linha = linhas[index].strip().split()
            escopo_tam = int(linha[0])
            escopo = list(map(lambda x: f'x{x}', linha[1:1 + escopo_tam]))
            index += 1

            linha = linhas[index].strip().split()
            num_tuplas = int(linha[0])

            lista_de_tuplas = []
            linha.pop(0)

            for i in range(num_tuplas*escopo_tam):
                linha[i] = int(linha[i])
                
            for i in range(num_tuplas):
                lista_de_tuplas.append(tuple(linha[escopo_tam*(i):(escopo_tam*i)+escopo_tam]))
                
            index += 1
            
            csp.add_constraint(tipo_restricao, escopo, lista_de_tuplas)

        else:
            print(f"Unexpected linha format: {linhas[index].strip()}")  # Debug
            break

    return csp

def is_consistent(csp, assignment, var, value):
    assignment[var] = value
    for constraint_type, scope, tuples in csp.constraints:
        if var in scope:
            # Collect assigned values for the scope variables
            values = tuple(assignment[v] for v in scope if assignment[v] is not None)
            if len(values) == len(scope):
                if constraint_type == 'V' and values not in tuples:
                    assignment[var] = None
                    return False
                if constraint_type == 'I' and values in tuples:
                    assignment[var] = None
                    return False
    assignment[var] = None
    return True

def backtrack(csp, assignment):    
    # Check if all variables are assigned
    if all(v is not None for v in assignment.values()):
        return assignment

    # Select an unassigned variable (using a simple strategy here)
    var = next((v for v in assignment if assignment[v] is None), None)
    if var is None:
        return None

    # Try all values in the domain of the selected variable
    for value in csp.domains[var]:
        if is_consistent(csp, assignment, var, value):
            assignment[var] = value
            result = backtrack(csp, assignment)
            if result:
                return result
            print(f"Backtracking from value {value} for {var}")
            # If assignment does not lead to a solution, reset the variable
            assignment[var] = None
    return None

def solve_csp(csp):
    assignment = {var: None for var in csp.variables}
    return backtrack(csp, assignment)

def print_solution(solution):
    if solution:
        for var in solution:
            print(f"{var} = {solution[var]}")
    else:
        print("INVIAVEL")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = 'saida.txt'
    with open("saida.txt", 'w') as arq:
        sys.stdout = arq
        csp = read_input(input_file)
        solution = solve_csp(csp)
        print_solution(solution)

    sys.stdout = sys.__stdout__
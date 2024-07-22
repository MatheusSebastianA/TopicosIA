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
    print(f"Num de variaveis: {num_var}")  # Debug
    index += 1

    for i in range(num_var):
        linha = linhas[index].strip().split()
        dom_tam = int(linha[0])
        dom_valores = list(map(int, linha[1:1 + dom_tam]))
        print(f"Variavel x{i+1} dominio: {dom_valores}")  # Debug
        csp.add_variable(f'x{i+1}', dom_valores)
        index += 1

    num_restricoes = int(linhas[index].strip())
    print(f"Num de restricoes: {num_restricoes}")  # Debug
    index += 1

    while index < len(linhas):
        if linhas[index].strip() in {'V', 'I'}:
            tipo_restricao = linhas[index].strip()
            print(f"Tipo de restricao: {tipo_restricao}")  # Debug
            index += 1

            linha = linhas[index].strip().split()
            escopo_tam = int(linha[0])
            escopo = list(map(lambda x: f'x{x}', linha[1:1 + escopo_tam]))
            print(f"Tamanho do escopo {escopo_tam}")
            print(f"Indices das variáveis do escopo {escopo}")  # Debug
            index += 1

            linha = linhas[index].strip().split()
            num_tuplas = int(linha[0])
            print(f"Num de tuplas: {num_tuplas}")  # Debug

            lista_de_tuplas = []
            linha.pop(0)
            for i in range(num_tuplas):
                lista_de_tuplas.append(tuple(linha[escopo_tam*(i):(escopo_tam*i)+escopo_tam]))
                
            print(lista_de_tuplas)
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
            values = tuple(assignment[v] for v in scope if assignment[v] is not None)
            if len(values) == len(scope):
                if constraint_type == 'V' and values not in tuples:
                    assignment[var] = None
                    return False
                if constraint_type == 'I' and values in tuples:
                    assignment[var] = None
                    return False
    return True

def backtrack(csp, assignment):
    if all(v is not None for v in assignment.values()):
        return assignment

    var = next(v for v in assignment if assignment[v] is None)
    for value in csp.domains[var]:
        if is_consistent(csp, assignment, var, value):
            result = backtrack(csp, assignment)
            if result:
                return result
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
    csp = read_input(input_file)
    solution = solve_csp(csp)
    print_solution(solution)
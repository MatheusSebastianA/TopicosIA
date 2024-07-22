import sys

class CSP:
    def __init__(self):
        self.variaveis = {}
        self.dominios = {}
        self.restricoes = []

    def add_variavel(self, var, domain):
        self.variaveis[var] = None
        self.dominios[var] = domain

    def add_restricao(self, tipo_restricao, escopo, tuplas):
        self.restricoes.append((tipo_restricao, escopo, tuplas))

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
        csp.add_variavel(f'x{i+1}', dom_valores)
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
            
            csp.add_restricao(tipo_restricao, escopo, lista_de_tuplas)
            

        else:
            print(f"Unexpected linha format: {linhas[index].strip()}") 
            break

    return csp

def is_consistent(csp, assignment, var, value):
    assignment[var] = value
    for tipo_restricao, escopo, tuplas in csp.restricoes:
        if var in escopo:
            values = tuple(assignment[v] for v in escopo if assignment[v] is not None)
            if len(values) == len(escopo):
                if tipo_restricao == 'V' and values not in tuplas:
                    assignment[var] = None
                    return False
                if tipo_restricao == 'I' and values in tuplas:
                    assignment[var] = None
                    return False
    assignment[var] = None
    return True

def backtrack(csp, assignment):    
    if all(v is not None for v in assignment.values()):
        return assignment

    var = next((v for v in assignment if assignment[v] is None), None)
    if var is None:
        return None

    for value in csp.dominios[var]:
        if is_consistent(csp, assignment, var, value):
            assignment[var] = value
            result = backtrack(csp, assignment)
            if result:
                return result
            print(f"Backtracking from value {value} for {var}")
            assignment[var] = None
    return None

def solve_csp(csp):
    assignment = {var: None for var in csp.variaveis}
    return backtrack(csp, assignment)

def print_solucao(sol):
    if sol:
        for var in sol:
            print(f"{var} = {sol[var]}")
    else:
        print("INVIAVEL")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = 'output.txt'
    with open(output_file, 'w') as arq:
        sys.stdout = arq
        csp = read_input(input_file)
        solucao = solve_csp(csp)
        print_solucao(solucao)

    sys.stdout = sys.__stdout__
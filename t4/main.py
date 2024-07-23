import sys
from collections import deque

class CSP:
    def __init__(self):
        self.variaveis = {}
        self.dominios = {}
        self.restricoes = []

    def add_variavel(self, var, domain):
        self.variaveis[var] = None
        self.dominios[var] = set(domain)

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

def ac3(csp):
    queue = deque()
    # Populate queue with all arcs
    for tipo_restricao, escopo, _ in csp.restricoes:
        for i in range(len(escopo)):
            for j in range(i + 1, len(escopo)):
                queue.append((escopo[i], escopo[j]))
    
    while queue:
        xi, xj = queue.popleft()
        if revise(csp.dominios, csp.restricoes, xi, xj):
            if not csp.dominios[xi]:
                return False
            for xk in get_related_vars(csp, xi):
                if xk != xj:
                    queue.append((xk, xi))
    return True

def get_related_vars(csp, var):
    related_vars = set()
    for tipo_restricao, escopo, _ in csp.restricoes:
        if var in escopo:
            related_vars.update(v for v in escopo if v != var)
    return related_vars

""" def revise(csp, xi, xj):
    revised = False
    to_remove = set()
    
    print(f"Revisando arcos ({xi}, {xj})")
    for x in csp.dominios[xi]:
        if not any((x, y) in tuples for y in csp.dominios[xj] for tipo, escopo, tuples in csp.restricoes if (xi in escopo and xj in escopo)):
            to_remove.add(x)
    
    if to_remove:
        print(f"Removendo valores de {xi}: {to_remove}")
        csp.dominios[xi].difference_update(to_remove)
        revised = True
    
    return revised
 """

def revise(domains, constraints, var1, var2):
    revised = False
    if (var1, var2) in constraints or (var2, var1) in constraints:
        # Obtém os domínios das variáveis
        domain1 = set(domains[var1])
        domain2 = set(domains[var2])
        
        # Calcula a interseção dos domínios
        intersection = domain1.intersection(domain2)
        
        # Verifica se o domínio da var1 precisa ser ajustado
        if intersection != domain1:
            domains[var1] = list(intersection)
            revised = True
            
    return revised

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

def select_mrv_variable(csp, assignment):
    min_domain_size = float('inf')
    mrv_var = None
    for var in csp.variaveis:
        if assignment[var] is None:
            domain_size = len(csp.dominios[var])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                mrv_var = var
    
    return mrv_var

def backtrack(csp, assignment):
    if all(v is not None for v in assignment.values()):
        return assignment
    
    if not ac3(csp):
        return None
    
    var = select_mrv_variable(csp, assignment)
    if var is None:
        return None

    for value in list(csp.dominios[var]):
        if is_consistent(csp, assignment, var, value):
            assignment[var] = value
            if var == 'x14':
                print(assignment)
            result = backtrack(csp, assignment)
            if result:
                return result
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

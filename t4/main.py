import sys
from collections import deque

class CSP:
    def __init__(self):
        self.variaveis = {}
        self.dominios = {}
        self.restricoes = []

    def add_variavel(self, var, dominio):
        self.variaveis[var] = None
        self.dominios[var] = set(dominio)

    def add_restricao(self, tipo_restricao, escopo, tuplas):
        self.restricoes.append((tipo_restricao, escopo, tuplas))

def le_entrada(file_path):
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
            linha.pop(0)

            lista_de_tuplas = []
            

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
    fila = deque()
    # Fila com todas os arcos a serem verificados
    for tipo_restricao, escopo, _ in csp.restricoes:
        for i in range(len(escopo)):
            for j in range(i + 1, len(escopo)):
                fila.append((escopo[i], escopo[j]))
    
    while fila:
        xi, xj = fila.popleft()
        if revisa(csp.dominios, csp.restricoes, xi, xj):
            if not csp.dominios[xi]:
                return False
            for xk in pega_var_relacionadas(csp, xi):
                if xk != xj:
                    fila.append((xk, xi))
    
    return True

def pega_var_relacionadas(csp, var):
    var_relacionadas = set()
    for tipo_restricao, escopo, _ in csp.restricoes:
        if var in escopo:
            var_relacionadas.update(v for v in escopo if v != var)
    return var_relacionadas


def revisa(dominios, restricoes, var1, var2):
    revisado = False
    # Encontra as restrições que envolvem var1 e var2
    restricoes_relacionadas = []
    tuplas_relacionadas = []
    escopos_relacionados = []
    for tipo_restricao, escopo, tuplas in restricoes:
        if var1 in escopo and var2 in escopo:
            restricoes_relacionadas.append((tipo_restricao, escopo, tuplas))
            tuplas_relacionadas.append(tuplas)
            escopos_relacionados.append(escopo)
    
    if not restricoes_relacionadas:
        return revisado
    
    
    """ Debug
    print(restricoes_relacionadas)
    print(escopos_relacionados)
    print(tuplas_relacionadas) 
    """
    
    x_i = (escopos_relacionados[0].index(var1))
    y_i = (escopos_relacionados[0].index(var2))
    
    remover_domV1 = []
    remover_domV2 = []
    nao_remover_domV1 = []
    nao_remover_domV2 = []
    

    for x in dominios[var1]:
        for y in dominios[var2]:
            for tupla in tuplas_relacionadas:
                for i in tupla:
                    if x == i[x_i] and y == i[y_i]:
                        if x not in nao_remover_domV1:
                            nao_remover_domV1.append(x)
                        if y not in nao_remover_domV2:  
                            nao_remover_domV2.append(y)
                    else:
                        if x not in remover_domV1:
                            remover_domV1.append(x)
                        if y not in remover_domV2: 
                            remover_domV2.append(y)

    for i in range (len(nao_remover_domV1)):
        remover_domV1.remove(nao_remover_domV1[i])
    for i in range (len(nao_remover_domV2)): 
        remover_domV2.remove(nao_remover_domV2[i])
    
    if remover_domV1:
        dominios[var1].difference_update(remover_domV1)
        dominios[var2].difference_update(remover_domV2)
        revisado = True

    return revisado

def eh_consistente(csp, atribuicao, var, valor):
    atribuicao[var] = valor
    for tipo_restricao, escopo, tuplas in csp.restricoes:
        if var in escopo:
            valors = tuple(atribuicao[v] for v in escopo if atribuicao[v] is not None)
            if len(valors) == len(escopo):
                if tipo_restricao == 'V' and valors not in tuplas:
                    atribuicao[var] = None
                    return False
                if tipo_restricao == 'I' and valors in tuplas:
                    atribuicao[var] = None
                    return False
    atribuicao[var] = None
    return True

def seleciona_var_mrv(csp, atribuicao):
    menor_dominio = float('inf')
    mrv_var = None
    for var in csp.variaveis:
        if atribuicao[var] is None:
            tam_dominio = len(csp.dominios[var])
            if tam_dominio < menor_dominio:
                menor_dominio = tam_dominio
                mrv_var = var
    return mrv_var

def backtrack(csp, atribuicao):
    if all(v is not None for v in atribuicao.values()):
        return atribuicao
    
    if not ac3(csp):
        return None
    
    var = seleciona_var_mrv(csp, atribuicao)
    if var is None:
        return None

    for valor in list(csp.dominios[var]):
        if eh_consistente(csp, atribuicao, var, valor):
            atribuicao[var] = valor
            resultado = backtrack(csp, atribuicao)
            if resultado:
                return resultado
            atribuicao[var] = None
    
    return None

def solve_csp(csp):
    atribuicao = {var: None for var in csp.variaveis}
    return backtrack(csp, atribuicao)

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
        csp = le_entrada(input_file)
        solucao = solve_csp(csp)
        print_solucao(solucao)

    sys.stdout = sys.__stdout__

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
            print(f"Formato de linha não esperado: {linhas[index].strip()}") 
            break

    return csp

def gac3(csp):
    pilha = deque()
    arcos_processados = set()
    
    # Empilha todos os arcos sem repetições
    if not pilha: 
        for tipo_restricao, escopo, _ in csp.restricoes:
            for i in range(len(escopo)):
                for j in range(i+1, len(escopo)):
                    if i != j:
                        arco = (escopo[i], escopo[j])
                        
                        if arco not in arcos_processados:
                            pilha.append(arco)
                            arcos_processados.add(arco)
                    
    while pilha:
        xi, xj = pilha.popleft()
        if revisa_gac(csp, xi):
            if not csp.dominios[xi]:
                return False
            for xk in pega_var_relacionadas_gac(csp, xi):
                if xk != xj:
                    arco = (xk, xi)
                    if arco not in arcos_processados:
                        pilha.append(arco)
                        arcos_processados.add(arco)

    return True


def revisa_gac(csp, xi):
    revisado = False
    valores_a_remover = set()

    for tipo_restricao, escopo, tuplas in csp.restricoes:
        if xi in escopo:
            xi_idx = escopo.index(xi)

            # Para cada valor em xi, verificar se há suporte nas outras variáveis do escopo
            for valor_xi in csp.dominios[xi]:
                suporte_encontrado = False
                for tupla in tuplas:
                    if valor_xi == tupla[xi_idx]:
                        suporte_encontrado = True
                        for var_idx, var in enumerate(escopo):
                            if var != xi:
                                if tupla[var_idx] not in csp.dominios[var]:
                                    suporte_encontrado = False
                                    break
                        if suporte_encontrado:
                            break
                if not suporte_encontrado:
                    valores_a_remover.add(valor_xi)

    if valores_a_remover:
        csp.dominios[xi].difference_update(valores_a_remover)
        revisado = True

    return revisado


def pega_var_relacionadas_gac(csp, var):
    var_relacionadas = set()
    for tipo_restricao, escopo, _ in csp.restricoes:
        if var in escopo:
            var_relacionadas.update(v for v in escopo if v != var)
    return var_relacionadas


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

    # Escolher a variável com o menor domínio restante
    var = seleciona_var_mrv(csp, atribuicao)
    if var is None:
        return None

    dominio_original = csp.dominios[var].copy()
    for valor in list(csp.dominios[var]):
        if eh_consistente(csp, atribuicao, var, valor):
            atribuicao[var] = valor
            # Criar uma cópia dos domínios antes da atribuição
            dominios_copia = {v: csp.dominios[v].copy() for v in csp.variaveis}
            # Atualizar o domínio com a atribuição e aplicar GAC
            csp.dominios[var] = {valor}
            if gac3(csp):
                resultado = backtrack(csp, atribuicao)
                if resultado:
                    return resultado
            # Restaurar os domínios após o backtrack
            csp.dominios = dominios_copia
            atribuicao[var] = None
    
    # Restaurar o domínio original antes de retornar
    csp.dominios[var] = dominio_original
    return None




def solve_csp(csp):
    atribuicao = {var: None for var in csp.variaveis}
    if not gac3(csp):
        return None
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
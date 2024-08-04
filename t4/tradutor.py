import sys

def read_dimacs(filename):
    """
    Lê o arquivo DIMACS e retorna o número de variáveis e uma lista de cláusulas.
    """
    num_vars = 0
    clausulas = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('p cnf'):
                _, _, num_vars, _ = line.split()
                num_vars = int(num_vars)
            elif line and not line.startswith('c'):
                # Remove o zero final e separa os literais da cláusula
                clausula = list(map(int, line.split()[:-1]))
                if clausula:  # Adiciona a cláusula se não estiver vazia
                    clausulas.append(clausula)

    return num_vars, clausulas

def converte_clausula(clausula):
    """
    Converte uma cláusula DIMACS em uma lista de restrições no formato do CSP solver.
    Cada cláusula é uma restrição no formato binário.
    """
    restricoes = []
    # Cada cláusula é uma restrição sozinha no formato desejado
    restricoes.append(clausula)
    return restricoes

def write_csp_format(num_vars, clausulas):
    tam_dominio = 2
    """
    Escreve o arquivo de saída no formato de restrições do CSP.
    """
    # Escreve o domínio das variáveis
    print(f"{num_vars}")
    for i in range(1, num_vars+1):
        print(f'{tam_dominio} {-1} {1}')

    # Escreve as restrições
    num_restricoes = len(clausulas)
    print(f"{num_restricoes}")
    for clausula in clausulas:
        restricoes = converte_clausula(clausula)
        for restricao in restricoes:
            print(f"V")
            print(f"{len(restricao)}", end=' ')
            for i in range (len(restricao)):
                if ('-' not in str(restricao[i])):
                    print(f"{restricao[i]}", end=' ')
                else:
                    print(f"{restricao[i] - (2*restricao[i])}", end=' ')

            print()
            print(f'{2**len(restricao) - 1}', end=' ')
            backtrack(len(restricao), restricao, [], 0)
            print()
            

def backtrack(len_restricao, restricao, valor_atual=[], ind=0):
    csp_sum = 0
    if ind == len_restricao:
        csp_assignment = [x if x == 1 else -1 for x in valor_atual]
        csp_sum = sum(csp_assignment[i] * (1 if restricao[i] > 0 else -1) for i in range(len_restricao))
        if csp_sum != -(len_restricao):
            print(' '.join(map(str, csp_assignment)), end=' ')
        
        return
    
    # Atribui -1 e chama a função recursivamente
    valor_atual.append(-1)
    backtrack(len_restricao, restricao, valor_atual, ind + 1)
    valor_atual.pop()
    
    # Atribui 1 e chama a função recursivamente
    valor_atual.append(1)
    backtrack(len_restricao, restricao, valor_atual, ind + 1)
    valor_atual.pop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Entrada errada, utilize: python3 tradutor.py > <input_file.txt> ")
        sys.exit(1)

    input_file = sys.argv[1]
    num_vars, clausulas = read_dimacs(input_file)
    write_csp_format(num_vars, clausulas)

    sys.stdout = sys.__stdout__

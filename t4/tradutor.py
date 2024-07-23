import sys

def read_dimacs(filename):
    """
    Lê o arquivo DIMACS e retorna o número de variáveis e uma lista de cláusulas.
    """
    num_vars = 0
    clauses = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('p cnf'):
                _, _, num_vars, _ = line.split()
                num_vars = int(num_vars)
            elif line and not line.startswith('c'):
                # Remove o zero final e separa os literais da cláusula
                clause = list(map(int, line.split()[:-1]))
                if clause:  # Adiciona a cláusula se não estiver vazia
                    clauses.append(clause)

    return num_vars, clauses

def convert_clause_to_constraints(clause):
    """
    Converte uma cláusula DIMACS em uma lista de restrições no formato do CSP solver.
    Cada cláusula é uma restrição no formato binário.
    """
    constraints = []
    # Cada cláusula é uma restrição sozinha no formato desejado
    constraints.append(clause)
    return constraints

def write_csp_format(num_vars, clauses):
    tam_dominio = 2
    positivos = 0
    negativos = 0
    """
    Escreve o arquivo de saída no formato de restrições do CSP.
    """
    # Escreve o domínio das variáveis
    print(f"{num_vars}")
    for i in range(1, num_vars+1):
        print(f'{tam_dominio} {-1} {1}')

    # Escreve as restrições
    num_constraints = len(clauses)
    print(f"{num_constraints}")
    for clause in clauses:
        constraints = convert_clause_to_constraints(clause)
        for constraint in constraints:
            print(f"V")
            print(f"{len(constraint)}", end=' ')
            for i in range (len(constraint)):
                if ('-' not in str(constraint[i])):
                    print(f"{constraint[i]}", end=' ')
                    positivos += 1
                else:
                    print(f"{constraint[i] - (2*constraint[i])}", end=' ')
                    negativos += 1
            print('')
            print(f'{2**len(constraint) - 1}', end=' ')
            print(backtrack(len(constraint), constraint, [], 0))
            

def backtrack(len_constraint, constraint, current_assignment=[], index=0):
    csp_sum = 0
    if index == len_constraint:
        csp_assignment = [x if x == 1 else -1 for x in current_assignment]
        csp_sum = sum(csp_assignment[i] * (1 if constraint[i] > 0 else -1) for i in range(len_constraint))
        if csp_sum != -(len_constraint):
            print(' '.join(map(str, csp_assignment)), end=' ')
        
        return
    
    # Atribui -1 e chama a função recursivamente
    current_assignment.append(-1)
    backtrack(len_constraint, constraint, current_assignment, index + 1)
    current_assignment.pop()
    
    # Atribui 1 e chama a função recursivamente
    current_assignment.append(1)
    backtrack(len_constraint, constraint, current_assignment, index + 1)
    current_assignment.pop()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tradutor.py <input_file.dimacs> <output_file.csp>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    num_vars, clauses = read_dimacs(input_file)
    
    with open(output_file, 'w') as arq:
        sys.stdout = arq
        write_csp_format(num_vars, clauses)

    sys.stdout = sys.__stdout__

Integrantes:
Guilherme Stonoga Tedardi - GRR20221241
Matheus Sebastian Alencar de Carvalho - GRR20220065

Forma de execução:

Se for um arquivo em formato DIMACS:
1º python3 tradutor.py <DIMACS.txt> > <input.txt>
2º python3 main.py <input.txt>
Importante ressaltar que o output de tradutor.py será o arquivo de entrada para o main.py e que o resultado é feito na saída padrão, sendo direcionada para o <input.txt> por >.
Já o arquivo main.py manda para um arquivo fixo "output.txt", caso esse arquivo já exista, ele será sobrescrito, caso não exista será criado.
<"arquivo"> = nome do arquivo que representa cada coisa, não precisa ser necessárimanete o nome especificado no comando de execução, só tem que seguir .

Se for um arquivo diretamente no formato do enunciado:
1º python3 main.py <input.txt>

Se for rodar o arquivo n-queens.c:
1º gcc n-queens.c -o n-queens
2º ./n-queens <n-rainhas> > <input.txt>
3º python3 main.py <input.txt>

Melhorias implementadas:
Tendo em vista que o trabalho 3 não foi implementado pela dupla, as melhorias foram baseadas na implementação do GAC3 e MRV, que foram solicitadas. Além disso, uma melhoria adotada para o tradutor foi selecionar todas as tuplas possíveis exceto aquela com garantia de erro, feito pela soma dos valores (-1, 1) e se a soma for igual a -(quantidade de literais) significa que essa tupla não satisfaz a cláusula.

Limitações: 

Detalhes:
O tradutor foi feito utilizando sempre um domínio de tamanho 2 e com valores {-1, 1}. A quantidade de restrições será sempre (2^n) - 1, tendo em vista que sempre alguma tupla não satisfaz a cláusula já que não apresenta repetição de variáveis (x1 ou ~x1, por exemplo).
Alguns prints podem ser encontrados ao longo do código para depuração
O tradutor apresenta as variáveis sem o -, para que não haja problema de leitura pelo main.py, mas os valores das restrições levam em consideração se a variável é negada na clásula.

Experimentos:
Para o problema das N-rainhas, a partir de N igual a 32 o programa demora cerca de 1 minuto para resolver, aumentando para os demais casos e ficando inviável para 16(demorou mais de 10 minutos).
Para o problema SAT, a partir de 100 variáveis o programa demora mais de 3 minutos para ser concluído, para 75 variáveis alguns demoram em torno de 20 segundos a 1 minuto.
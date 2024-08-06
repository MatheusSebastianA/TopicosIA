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

Não conseguimos executar o programa em python como forma de solver para o mundo de wumpus em C. Acreditamos que seja pelo formato do programa main.py.

Melhorias implementadas:
Tendo em vista que o trabalho 3 não foi implementado pela dupla, as melhorias foram baseadas na implementação do GAC3 e MRV, que foram solicitadas. Em questões de estrutura não fizemos nenhum melhoria pois não tínhamos no que nos basear para melhorar. Favor levar em consideração para a correção que o T3 não foi implementado.

Limitações: 

Detalhes:
O tradutor foi feito utilizando sempre um domínio de tamanho 2 e com valores {-1, 1}. A quantidade de restrições será sempre (2^n) - 1, tendo em vista que sempre alguma tupla não satisfaz a cláusula, já que não apresenta repetição de variáveis (x1 ou ~x1, por exemplo).
O tradutor apresenta as variáveis sem o -, para que não haja problema de leitura pelo main.py, mas os valores das restrições levam em consideração se a variável é negada na clásula.

Experimentos:
Para o problema das N-rainhas, a partir de N igual a 35 o programa demora cerca de 2 minutos para resolver, aumentando para os demais casos e ficando inviável para 40(demorou mais de 10 minutos).
Para o problema SAT, a partir de 100 variáveis o programa demora mais de 3 minutos para ser concluído, para 75 variáveis alguns demoram em torno de 20 segundos a 2 minutos.

Detalhes de implementação:
Após conversar com o professor, vimos que a aplicação do GAC3 para cada atribuição dentro do backtrack aumenta exponencialmente o tempo de execução do programa, para título de comparação, antes dessa implementação o código funcionava, em tempo viável, para o problema das N-rainhas, com um tamanho 16.
Com essa implementação, tantos os problemas SAT quanto os das N-rainhas tiveram uma melhora substancial.

Comentários:
Foi enviado um tar.gz com todos os arquivos necessários para testar o problema SAT (DIMACS.txt) e o N-rainhas(n-queens.o e n-queens.c). Além disso, foi enviado também os arquivos <input.txt> com o problema das N-rainhas = 35 e o <output.txt> com o resultado dessa entrada.
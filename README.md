# sisIntTabuleiro

# Topicos Principais
- Traçar uma rota na qual tem INICIO e FIM. Terá obstaculos no caminho que deverá ser desviados.
- Caso esteja enxergando o ponto final. Ir direto pra ele
- Caso não esteja enxergando, vai ter que navegar pelos vertices até chegar ao destino.

# Restrições
1. Você so poderá sair de um vertice para o outro.
2. Terá que andar em linha reta a qualquer ponto que estará visivel ao ponto de partida.
3. Não pode atravessar um obstaculo.
4. Irá mudar a quantidade de obstáculos, para verificar se realmente não está havendo colisões.
5. Pode andar sobre as arestas dos obstaculos. Porém não pode é atravessálos. Mas poderá andar nas extremidades. Como se eles estivesse desviando do obstaculo. 

# Como Fazer pra ver se está atravessando um obstaculo?
- voces vão ter que interpretar esses pontos(pontos dos obstaculos) como retas.
- tem que calcular se um segmento de reta, Faz interceção com outro segmento de reta
- existe uma equação que calcula se um segmento de reta A e outro segmento de reta B tem uma intercação.(basicamente calcular um determinante)

# parâmetros
1. Um ponto INICIAL e um ponto FINAL. (fixos)
2. Quantidade de obstaculos (variavel)
3. Desenhar os obstaculos em locais aleatórios, e um obstaculo não vai poder sobrepor outro. 
4. tamanho do obstaculo (fixo)


# Objetivo Final do Trabalho
- Encontrar uma rota qualquer. Sem passar pelos obstaculos.

# Etapa 1:
Plotar o mapa

# Etapa 2:
Encontrar todas as arestas possíveis, ou seja encontrar todas as retas possiveis de uma aresta até a outra sem atravessar um obstaculo

# Ultima Etapa:
Encontrar uma rota que vá do ponto inicial ao final sem atravessar nenhum osbatculo
O plot final deve ficar com todas as possiveis arestas desenhadas e a rota final encontrada(de uma cor diferente das arestas plotadas) pelo algoritmo implementado.

# Cuidado:
Dependendo do algoritmo que seja utilizado para implementar a questão de encontrar a rota, possa ser que ele fique em loop infinito arrudiando um obstaculo. 

# Medida de precausão:
Sempre salvar as arestas pelas quais a rota ja passou. E sempre verificar se ja foi passado naquela aresta. 
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from collections import defaultdict
import matplotlib.patches as patches


# Configuração do tabuleiro
largura_tabuleiro = int(input("Digite a largura do tabuleiro: "))
altura_tabuleiro = int(input("Digite a altura do tabuleiro: "))
num_obstaculos = int(input("Digite a quantidade de obstáculos: "))

# Função para aumentar o tabuleiro até caber os obstáculos
def aumentar_tabuleiro(largura, altura, num_obstaculos):
    area_tabuleiro = largura * altura
    while area_tabuleiro < num_obstaculos * 2:  # Multiplica por 2 para dar mais espaço
        largura += 2
        altura += 2
        area_tabuleiro = largura * altura
    return largura, altura

# Aumenta o tamanho do tabuleiro se necessário
largura_tabuleiro, altura_tabuleiro = aumentar_tabuleiro(largura_tabuleiro, altura_tabuleiro, num_obstaculos)

# Ponto inicial e final
ponto_inicial = (0, 0)
ponto_final = (largura_tabuleiro - 1, altura_tabuleiro - 1)

# Lista para armazenar os obstáculos
obstaculos = []

# Função para calcular a distância entre dois pontos
def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Função para adicionar obstáculos respeitando a distância mínima
def adicionar_obstaculo():
    tentativas = 0
    while len(obstaculos) < num_obstaculos:
        novo_x = random.uniform(0.5, largura_tabuleiro - 0.5)
        novo_y = random.uniform(0.5, altura_tabuleiro - 0.5)
        novo_obstaculo = (novo_x, novo_y)

        # Verifica colisões com obstáculos existentes, ponto inicial e ponto final
        colisao = any(calcular_distancia(novo_obstaculo, obst) < 1.5 for obst in obstaculos) or \
                  calcular_distancia(novo_obstaculo, ponto_inicial) < 1.5 or \
                  calcular_distancia(novo_obstaculo, ponto_final) < 1.5

        if not colisao:
            obstaculos.append(novo_obstaculo)
        
        tentativas += 1
        if tentativas > 1000:
            print("Não foi possível alocar todos os obstáculos devido ao espaço limitado.")
            break

# Adicionar obstáculos
adicionar_obstaculo()

# Função para verificar se um ponto está dentro de um obstáculo
def ponto_dentro_obstaculo(ponto):
    for obs in obstaculos:
        obstaculo_x, obstaculo_y = obs
        if (abs(ponto[0] - obstaculo_x) < 0.5 and abs(ponto[1] - obstaculo_y) < 0.5):
            return True
    return False

def verificar_intersecao(p1, p2, p3, p4):
    def orientacao(A, B, C):
        # Calcula a área do triângulo formado por A, B e C
        return (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])

    # Verifica se as orientações cruzadas são diferentes
    o1 = orientacao(p1, p2, p3)
    o2 = orientacao(p1, p2, p4)
    o3 = orientacao(p3, p4, p1)
    o4 = orientacao(p3, p4, p2)

    # Se os sinais das orientações são opostos, os segmentos se cruzam
    return (o1 * o2 < 0) and (o3 * o4 < 0)


# Função para verificar se o segmento de reta entre dois pontos cruza algum obstáculo
def verifica_cruzamento_obstaculo(p1, p2):
    # Se algum dos pontos estiver dentro de um obstáculo, retornar True
    if ponto_dentro_obstaculo(p1) or ponto_dentro_obstaculo(p2):
        return True
    
    for obs in obstaculos:
        # Para cada obstáculo, verificamos as 4 arestas do quadrado
        obstaculo_x, obstaculo_y = obs
        canto_sup_esq = (obstaculo_x - 0.5, obstaculo_y + 0.5)
        canto_sup_dir = (obstaculo_x + 0.5, obstaculo_y + 0.5)
        canto_inf_esq = (obstaculo_x - 0.5, obstaculo_y - 0.5)
        canto_inf_dir = (obstaculo_x + 0.5, obstaculo_y - 0.5)
        
        # Verificar interseção com as 4 arestas do obstáculo
        if (verificar_intersecao(p1, p2, canto_sup_esq, canto_sup_dir) or  # Aresta superior
            verificar_intersecao(p1, p2, canto_sup_dir, canto_inf_dir) or  # Aresta direita
            verificar_intersecao(p1, p2, canto_inf_dir, canto_inf_esq) or  # Aresta inferior
            verificar_intersecao(p1, p2, canto_inf_esq, canto_sup_esq)):   # Aresta esquerda
            return True
    
    return False

def gerar_vertices():
    vertices = [ponto_inicial, ponto_final]
    
    # Adicionar os 4 cantos de cada obstáculo como vértices
    for obs in obstaculos:
        obstaculo_x, obstaculo_y = obs
        # Use exact coordinates for corners to avoid floating-point issues
        vertices.append((obstaculo_x - 0.5, obstaculo_y + 0.5))  # Canto superior esquerdo
        vertices.append((obstaculo_x + 0.5, obstaculo_y + 0.5))  # Canto superior direito
        vertices.append((obstaculo_x - 0.5, obstaculo_y - 0.5))  # Canto inferior esquerdo
        vertices.append((obstaculo_x + 0.5, obstaculo_y - 0.5))  # Canto inferior direito
    
    # More strict filtering of duplicate vertices
    vertices_unicos = []
    for v in vertices:
        is_duplicate = False
        for existing in vertices_unicos:
            if calcular_distancia(v, existing) < 1e-6:  # Stricter threshold
                is_duplicate = True
                break
        if not is_duplicate:
            vertices_unicos.append(v)
    
    return vertices_unicos

# Função para encontrar todas as arestas possíveis entre os vértices
def encontrar_arestas(vertices):
    grafo = defaultdict(list)
    arestas = []

    # Verificar a visibilidade entre cada par de vértices
    for i, v1 in enumerate(vertices):
        for j, v2 in enumerate(vertices):
            if i != j:  # Não criar arestas do vértice para ele mesmo
                # Verificar se é possível ir de v1 para v2 sem cruzar obstáculos
                if not verifica_cruzamento_obstaculo(v1, v2):
                    # Adicionar aresta em ambas as direções para criar um grafo não direcionado
                    grafo[i].append(j)
                    grafo[j].append(i)
                    arestas.append((v1, v2))

    return grafo, arestas


# Função para encontrar um caminho qualquer utilizando busca em largura (BFS)
def encontrar_caminho(grafo, vertices):
    from collections import deque

    # Fila para armazenar os caminhos parciais
    fila = deque([[0]])  # Começa com o índice do ponto inicial
    visitados = set([0])  # Conjunto para verificar os nós visitados

    while fila:
        caminho_atual = fila.popleft()
        ultimo_vertice = caminho_atual[-1]

        # Verifica se chegou ao ponto final
        if ultimo_vertice == 1:  # Índice 1 corresponde ao ponto final
            return [vertices[i] for i in caminho_atual]

        # Explora os vizinhos não visitados
        for vizinho in grafo[ultimo_vertice]:
            if vizinho not in visitados:
                novo_caminho = list(caminho_atual) + [vizinho]
                fila.append(novo_caminho)
                visitados.add(vizinho)

    # Se não encontrou um caminho, retorna None
    return None



# Função para plotar o grafo de visibilidade
def plotar_grafo_visibilidade(vertices, arestas, caminho=None):
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Função de zoom
    def zoom_factory(ax, base_scale=1.5):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            xdata = event.xdata  # Coordenada do mouse em x
            ydata = event.ydata  # Coordenada do mouse em y

            if event.button == 'up':
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                scale_factor = base_scale
            else:
                return

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_xlim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
            plt.draw()

        fig.canvas.mpl_connect('scroll_event', zoom)

    zoom_factory(ax)

    # Plota os obstáculos como quadrados azuis
    for obstaculo in obstaculos:
        ax.add_patch(patches.Rectangle((obstaculo[0] - 0.5, obstaculo[1] - 0.5), 1, 1,
                                       color='lightblue', alpha=0.7, edgecolor='blue'))

    # Contador de arestas plotadas
    num_arestas = len(arestas)
    print(f"Número de arestas plotadas: {num_arestas}")

    # Plota as arestas possíveis (grafo de visibilidade)
    for aresta in arestas:
        ax.plot([aresta[0][0], aresta[1][0]], [aresta[0][1], aresta[1][1]], 
                color='black', alpha=0.5, linewidth=0.5)

    # Exibe a quantidade de arestas no gráfico
    ax.text(0.02, 0.98, f'Arestas: {num_arestas}', transform=ax.transAxes,
            fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    # Plota todos os vértices como pontos pretos
    for i, v in enumerate(vertices):
        if i > 1:  # Não é o ponto inicial nem final
            ax.plot(v[0], v[1], 'o', color='black', markersize=5)

    # Plota o caminho encontrado
    if caminho:
        for i in range(len(caminho) - 1):
            ax.plot([caminho[i][0], caminho[i + 1][0]],
                    [caminho[i][1], caminho[i + 1][1]], 'r-', linewidth=1.5)

    # Plota os pontos inicial e final com destaque
    ax.plot(ponto_inicial[0], ponto_inicial[1], 'o', color='green', markersize=10, label='Início')
    ax.plot(ponto_final[0], ponto_final[1], 'o', color='red', markersize=10, label='Fim')

    # Configura os limites do gráfico
    ax.set_xlim(-1, largura_tabuleiro + 1)
    ax.set_ylim(-1, altura_tabuleiro + 1)
    ax.set_aspect('equal')

    plt.title("Grafo de Visibilidade (Zoom Interativo)")
    plt.legend()
    plt.show()



# Função principal
def main():
    print(f"Tamanho do tabuleiro: {largura_tabuleiro}x{altura_tabuleiro}")
    print(f"Número de obstáculos: {len(obstaculos)}")
    print(f"Ponto inicial: {ponto_inicial}, Ponto final: {ponto_final}")
    
    # Gerar vértices (cantos dos obstáculos + pontos inicial e final)
    vertices = gerar_vertices()
    print(f"Número de vértices: {len(vertices)}")
    
    # Encontrar arestas possíveis
    grafo, arestas = encontrar_arestas(vertices)
    print(f"Número de arestas possíveis: {len(arestas)}")
    
    # Encontrar caminho
    caminho = encontrar_caminho(grafo, vertices)
    
    if caminho:
        print(f"Caminho encontrado com {len(caminho)} vértices!")
    else:
        print("Não foi possível encontrar um caminho!")
    
    # Plotar o grafo de visibilidade
    plotar_grafo_visibilidade(vertices, arestas, caminho)

if __name__ == "__main__":
    main()
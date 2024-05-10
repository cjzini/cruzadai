import os

caminho = os.getcwd() + '/uploads/cruzada1.txt'
linhas = {}
palavras_ordenadas = {}
palavras = []
pistas = []


# Ler o arquivo e separar as palavras e as pistas, colocando em duas listas distintas
def ler_arquivo(caminho):
    with open(caminho, 'r') as arquivo:
        for linha in arquivo:
            conteudo = linha.split(':')
            linhas[conteudo[0]] = conteudo[1].rstrip('\n')

# Ordena o dicionário de acordo com o tamanho da palavra em ordem decrescente
# e retorna as duas listas de palavras e de pistas
def ordena_palavras(linhas):
    ordenado = dict(sorted(linhas.items(), key=lambda x: len(x[0]), reverse=True))
    palavras = list(ordenado.keys())
    pistas = list(ordenado.values())
    return palavras, pistas

def encontrar_interseccoes(quadro, palavra):
    interseccoes = []
    for i, linha in enumerate(quadro):
        for j, letra in enumerate(linha):
            if letra == palavra[0]:
                interseccoes.append((i, j))
    return interseccoes

def verificar_interferencia(quadro, palavra, posicao):
    for i, letra in enumerate(palavra):
        if quadro[posicao[0] + i][posicao[1]] != letra:
            return True
    return False

def adicionar_palavra(quadro, palavra, posicao):
    for i, letra in enumerate(palavra):
        quadro[posicao[0] + i][posicao[1]] = letra

def imprimir_quadro(quadro):
    for linha in quadro:
        print(" ".join(linha))

def criar_quadro(palavras):
    # Inicializa o quadro com uma grade vazia
    tamanho_maximo = len(palavras[0])
    tamanho_maximo = round(tamanho_maximo + (tamanho_maximo / 2))
    quadro = [[' ' for _ in range(tamanho_maximo)] for _ in range(tamanho_maximo)]

    for palavra in palavras:
        interseccoes = encontrar_interseccoes(quadro, palavra)

        for intersecao in interseccoes:
            if verificar_interferencia(quadro, palavra, intersecao):
                continue
            else:
                adicionar_palavra(quadro, palavra, intersecao)
                break
        else:
            # Se não houver uma posição adequada, você pode lidar com isso de acordo com seus requisitos
            print(f'Não foi possível encontrar uma posição para a palavra: {palavra}')

    return quadro

ler_arquivo(caminho)
palavras, pistas = ordena_palavras(linhas)
quadro_palavras_cruzadas = criar_quadro(palavras)
imprimir_quadro(quadro_palavras_cruzadas)

#print(palavras)
#print(pistas)
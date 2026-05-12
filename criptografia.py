def criptografar(entrada):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    matriz = [
        [2, 1],
        [1, 1]
    ]

    entrada = entrada.upper()
    if len(entrada) % 2 != 0:
        entrada += "X" 

    # Converte cada caractere para seu indice (posicao) no alfabeto
    numeros = [alfabeto.index(x) for x in entrada]
    resultado = []

    # Separa em blocos (vetores) de 2
    for i in range(0, len(numeros), 2):
        bloco = [numeros[i], numeros[i+1]]
        
        for coluna in range(2):
            soma = 0
            # Multiplicacao da matriz
            for linha in range(2):
                soma += bloco[linha] * matriz[linha][coluna]
            
            resultado.append(soma % 36)

    # Transforma os indices de volta para caracteres do alfabeto e os junta numa string
    return "".join([alfabeto[n] for n in resultado])

def descriptografar(entrada, tamanho):
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    matriz_inversa = [
        [1, 35],
        [35, 2]
    ]

    numeros = [alfabeto.index(x) for x in entrada.upper()]
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = [numeros[i], numeros[i+1]]
        
        for coluna in range(2):
            soma = 0
            for linha in range(2):
                soma += bloco[linha] * matriz_inversa[linha][coluna]
            resultado.append(soma % 36)

    entrada = "".join([alfabeto[n] for n in resultado])
    
    return entrada[:tamanho]

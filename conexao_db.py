import mysql.connector
import random
import criptografia
import os

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='eleicao_db',
)
cursor = conexao.cursor()


# ---------- Inserir um novo eleitor ----------
def inserir_eleitor(nome_eleitor, titulo_eleitor, cpf, mesario, chave_acesso):
    # Remove pontuação do CPF e título antes de validar
    cpf = limpar_numeros(cpf)
    titulo_eleitor = limpar_numeros(titulo_eleitor)

    if validar_cpf(cpf) == 0:
        print("Erro: CPF inválido!")
        return

    if validar_titulo(titulo_eleitor) == 0:
        print("Erro: Título de Eleitor inválido!")
        return

    # Criptografia
    chave_acesso = gerar_chave(nome_eleitor)
    chave_criptografada  = criptografia.criptografar(chave_acesso)
    cpf_criptografado    = criptografia.criptografar(cpf)
    titulo_criptografado = criptografia.criptografar(titulo_eleitor)
    try:
        if not conexao.is_connected():
            conexao.reconnect(attempts=3, delay=1)
        sql = "INSERT INTO eleitores (nome_eleitor, titulo_eleitor, cpf, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome_eleitor, titulo_criptografado, cpf_criptografado, mesario, chave_criptografada)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"\nEleitor inserido com sucesso!")
        print(f"Chave de Acesso Gerada (Anote, pois não será exibida novamente): {chave_acesso}")
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            print(f"\n[ERRO] Já existe um eleitor cadastrado com este CPF ou Título de Eleitor!")
        else:
            print(f"Erro ao inserir no banco: {erro}")
            conexao.rollback()

# ---------- Inserir candidato ----------
def inserir_candidato(nome_candidato, numero_votacao, partido):
    try:
        if not conexao.is_connected():
            conexao.reconnect(attempts=3, delay=1)
        sql = "INSERT INTO candidatos (nome_candidato, numero_votacao, partido) VALUES (%s, %s, %s)"
        valores = (nome_candidato, numero_votacao, partido)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"\nCandidato '{nome_candidato}' cadastrado com sucesso! ID: {cursor.lastrowid}")
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            print(f"\n[ERRO] Já existe um candidato com este número de votação!")
        else:
            print(f"Erro ao inserir candidato: {erro}")
            conexao.rollback()


# ---------- Validação de CPF ----------
def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return 0
    # Bloqueia repetição do mesmo número
    if cpf == cpf[0] * 11:
        return 0
    # Cálculo do primeiro dígito verificador
    soma1 = 0
    multiplicador = 10
    for i in range(9):
        soma1 = soma1 + (int(cpf[i]) * multiplicador)
        multiplicador = multiplicador - 1
    resto1 = soma1 % 11
    if resto1 < 2:
        verificador1 = 0
    else:
        verificador1 = 11 - resto1
    if int(cpf[9]) != verificador1:
        return 0
    # Cálculo do segundo dígito verificador
    soma2 = 0
    multiplicador = 11
    for i in range(10):
        soma2 = soma2 + (int(cpf[i]) * multiplicador)
        multiplicador = multiplicador - 1
    resto2 = soma2 % 11
    if resto2 < 2:
        verificador2 = 0
    else:
        verificador2 = 11 - resto2
    if int(cpf[10]) == verificador2:
        return 1
    else:
        return 0


# ---------- Validação do Título de Eleitor ----------
def validar_titulo(titulo):
    if len(titulo) != 12 or not titulo.isdigit():
        return 0
    sequencial = titulo[:8]
    uf = titulo[8:10]
    digito_verificador = titulo[10:] #dv
    soma = 0
    peso = [2, 3, 4, 5, 6, 7, 8, 9]

    # Cálculo do dígito verificador 1
    for i in range(8):
        soma += int(sequencial[i]) * peso[i]
    resto = soma % 11

    if resto == 10:
        dv1 = 0
    elif resto == 0 and uf in ['01', '02']:
        dv1 = 1
    else:
        dv1 = resto

    # Cálculo do dígito verificador 2
    soma2 = (int(uf[0]) * 7) + (int(uf[1]) * 8) + (dv1 * 9)
    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and uf in ['01', '02']:
        dv2 = 1
    else:
        dv2 = resto2

    dv_results = f"{dv1}{dv2}"
    if dv_results == digito_verificador:
        return 1 # título valido
    else:
        return 0 # título inválido


# ---------- Gerar Chave ----------
def gerar_chave(nome):
    nome = limpar_entrada(nome)
    parte_do_nome = nome[0] + nome[1] + nome[2]
    partes_nome = nome.split()
    if len (partes_nome) >= 2:
        primeiro_nome = partes_nome[0]
        segundo_nome = partes_nome[1]
        parte_do_nome = primeiro_nome[:2] + segundo_nome[0]
    else:
        parte_do_nome = nome[:3]
    numero_aleatorio = random.randint(1000, 9999)
    chave = str(parte_do_nome).upper() + str(numero_aleatorio)
    return chave


# Limpar acentos
def limpar_entrada(entrada):
    entrada = entrada.upper()
    com_acento = "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ"
    sem_acento = "AAAAAEEEEIIIIOOOOOOUUUUCN"
    for i in range(len(com_acento)):
        entrada = entrada.replace(com_acento[i], sem_acento[i])
    return entrada
# Remover a pontuação dos documentos
def limpar_numeros(entrada):
    return ''.join(c for c in entrada if c.isdigit())


# ---------- Buscar todos os usuários ----------
def listar_eleitores():
    cursor.execute("SELECT id_eleitor, nome_eleitor, titulo_eleitor, cpf, mesario FROM eleitores")
    for (id_eleitor, nome_eleitor, titulo_eleitor, cpf, mesario) in cursor.fetchall():
        print(f"ID: {id_eleitor}, Nome: {nome_eleitor}, Título: {titulo_eleitor}, CPF: {cpf}, Mesário: {mesario}")

def listar_candidatos():
    cursor.execute("SELECT id_candidato, nome_candidato, numero_votacao, partido FROM candidatos")
    for (id_candidato, nome_candidato, numero_votacao, partido) in cursor.fetchall():
        print(f"ID: {id_candidato}, Nome: {nome_candidato}, Número: {numero_votacao}, Partido: {partido}")


# ---------- Busca específica de eleitor ----------
def busca_eleitor(entrada):
    entrada = limpar_numeros(entrada)
    entrada_criptografada = criptografia.criptografar(entrada)
    comando = "SELECT nome_eleitor, cpf, chave_acesso FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"
    cursor.execute(comando, (entrada_criptografada, entrada_criptografada))
    resultado = cursor.fetchone()
    if resultado:
        print(f"\nResultado encontrado:")
        print(f"Nome: {resultado[0]}")
        print(f"CPF: {criptografia.descriptografar(resultado[1], 11)}")
        print(f"Chave de Acesso: {criptografia.descriptografar(resultado[2], 7)}")
    else:
        print("\nEleitor não localizado.")


# ---------- Resultados ----------
def boletim_urna():
    cursor.execute("""
        SELECT c.nome_candidato, c.partido, COUNT(v.id_candidato) AS total_votos
        FROM candidatos c
        LEFT JOIN votos v ON c.id_candidato = v.id_candidato
        GROUP BY c.id_candidato, c.nome_candidato, c.partido
        ORDER BY total_votos DESC
    """)
    resultados = cursor.fetchall()
    print(f"\n{'Nome':<30} {'Partido':<25} {'Votos':>6}")
    print("-" * 65)
    for (nome, partido, total) in resultados:
        print(f"{nome:<30} {partido:<25} {total:>6}")

    # Votos nulos/brancos
    cursor.execute("SELECT COUNT(*) FROM votos WHERE id_candidato IS NULL")
    nulos = cursor.fetchone()[0]
    print("-" * 65)
    print(f"{'Branco/Nulo':<30} {'':<25} {nulos:>6}")


def estatistica_comparecimento():
    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]
    ausentes = total_eleitores - total_votos
    percentual = (total_votos / total_eleitores * 100) if total_eleitores > 0 else 0

    print(f"\nTotal de eleitores cadastrados : {total_eleitores}")
    print(f"Total de votos computados      : {total_votos}")
    print(f"Ausentes                       : {ausentes}")
    print(f"Percentual de comparecimento   : {percentual:.2f}%")


def votos_por_partido():
    cursor.execute("""
        SELECT c.partido, COUNT(v.id_candidato) AS total_votos
        FROM candidatos c
        LEFT JOIN votos v ON c.id_candidato = v.id_candidato
        GROUP BY c.partido
        ORDER BY total_votos DESC
    """)
    resultados = cursor.fetchall()
    print(f"\n{'Partido':<30} {'Votos':>6}")
    print("-" * 38)
    for (partido, total) in resultados:
        print(f"{partido:<30} {total:>6}")


def listar_protocolos():
    cursor.execute("""
        SELECT v.protocolo_votacao, v.data_votacao, e.nome_eleitor
        FROM votos v
        JOIN eleitores e ON v.id_eleitor = e.id_eleitor
        ORDER BY v.data_votacao
    """)
    resultados = cursor.fetchall()
    if not resultados:
        print("\nNenhum voto registrado ainda.")
        return
    print(f"\n{'Protocolo (criptografado)':<28} {'Data/Hora':<22} {'Eleitor'}")
    print("-" * 75)
    for (protocolo, data, nome) in resultados:
        print(f"{protocolo:<28} {str(data):<22} {nome}")


# ---------- Fechar conexão ----------
def fechar_conexao():
    cursor.close()
    conexao.close()

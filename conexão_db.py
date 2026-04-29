import mysql.connector
import random

# Conexão com o banco ***** ESTÁ NO MEU BD EDUCACIONAL - RAMIRO ********
conexao = mysql.connector.connect(
    host='BD-ACD',
    user='BD120226732',
    password='Fwyjy4',
    database='BD120226732',
)
cursor = conexao.cursor()

# ---------- Inserir um novo usuário ----------
def inserir_eleitor(nome_eleitor, titulo_eleitor, cpf, mesario, chave_acesso):
# Verificação CPF
    resultado_cpf = validar_cpf(cpf)
    if resultado_cpf == 0:
        print("Erro: Esse CPF não existe!")
        return
# Verificação título
    resultado_titulo = validar_titulo(titulo_eleitor)
    if resultado_titulo == 0:
        print("Erro: Título errado!")
        return
# Passou nas duas verificações:
    chave_acesso = gerar_chave(nome_eleitor)
    try:
        if not conexao.is_connected():
            conexao.reconnect(attempts=3, delay=1)
        sql = "INSERT INTO eleitores (nome_eleitor, titulo_eleitor, cpf, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome_eleitor, titulo_eleitor, cpf, mesario, chave_acesso)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Eleitor inserido com Sucesso!")
        print(f"Chave de Acesso Gerada: {chave_acesso}")
    except mysql.connector.Error as erro:
        print(f"Erro ao inserir no banco: {erro}")
        conexao.rollback()

def inserir_candidato(nome_candidato, numero_votacao, partido):
    sql = "INSERT INTO candidatos (nome_candidato, numero_votacao, partido) VALUES (%s, %s, %s)"
    valores = (nome_candidato, numero_votacao, partido)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Candidato inserido com ID:", cursor.lastrowid)

# ---------- Validação de CPF ----------
def validar_cpf(cpf):
    if len(cpf) != 11:
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
        
# ---------- Validação do Título ----------
def validar_titulo(titulo):
    if len(titulo) == 12:
        return 1
    else:
        return 0
    
# ---------- Gerar Chave ----------
def gerar_chave(nome):
    parte_do_nome = nome[0] + nome[1] + nome[2]
    numero_aleatorio = random.randint(1000, 9999)
    chave = str(parte_do_nome).upper() + str(numero_aleatorio)
    return chave

# ---------- Buscar todos os usuários ----------
def listar_eleitores():
    cursor.execute("SELECT id_eleitor, nome_eleitor, titulo_eleitor, cpf, mesario FROM eleitores")
    for (id_eleitor, nome_eleitor, titulo_eleitor, cpf, mesario) in cursor.fetchall():
        print(f"ID: {id_eleitor}, Nome: {nome_eleitor}, Título de Eleitor: {titulo_eleitor}, CPF: {cpf}, Mesário: {mesario}")

def listar_candidatos():
    cursor.execute("SELECT id_candidato, nome_candidato, numero_votacao, partido FROM candidatos")
    for (id_candidato, nome_candidato, numero_votacao, partido) in cursor.fetchall():
        print(f"ID: {id_candidato}, Nome: {nome_candidato}, Número de Votação: {numero_votacao}, Partido: {partido}")

# ---------- Busca específica de eleitor ----------

def busca_eleitor(entrada):
    comando = "SELECT nome_eleitor, cpf, chave_acesso FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"
    cursor.execute(comando, (entrada, entrada))
    resultado = cursor.fetchone()
    if resultado:
        print(f"\nResultado encontrado:")
        print(f"Nome: {resultado[0]}")
        print(f"CPF: {resultado[1]}")
        print(f"Chave de Acesso: {resultado[2]}")
    else:
        print("\nEleitor não localizado")

# Fechar conexão **** FAZER FUNÇÃO PARA FECHAR CONEXÃO *****

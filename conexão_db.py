import mysql.connector


# Conexão com o banco
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='SENHA',
    database='eleição_db'
)
cursor = conexao.cursor()


# ---------- Inserir um novo usuário ----------
def inserir_eleitor(nome_eleitor, titulo_eleitor, cpf, mesario):
    sql = "INSERT INTO eleitores (nome_eleitor, titulo_eleitor, cpf, mesario) VALUES (%s, %s, %s, %s)"
    valores = (nome_eleitor, titulo_eleitor, cpf, mesario)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Eleitor inserido com ID:", cursor.lastrowid)

def inserir_candidato(nome_candidato, numero_votacao, partido):
    sql = "INSERT INTO candidatos (nome_candidato, numero_votacao, partido) VALUES (%s, %s, %s)"
    valores = (nome_candidato, numero_votacao, partido)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Candidato inserido com ID:", cursor.lastrowid)


# ---------- Buscar todos os usuários ----------
def listar_eleitores():
    cursor.execute("SELECT id_eleitor, nome_eleitor, titulo_eleitor, cpf, mesario FROM eleitores")
    for (id_eleitor, nome_eleitor, titulo_eleitor, cpf, mesario) in cursor.fetchall():
        print(f"ID: {id_eleitor}, Nome: {nome_eleitor}, Título de Eleitor: {titulo_eleitor}, CPF: {cpf}, Mesário: {mesario}")

def listar_candidatos():
    cursor.execute("SELECT id_candidato, nome_candidato, numero_votacao, partido FROM candidatos")
    for (id_candidato, nome_candidato, numero_votacao, partido) in cursor.fetchall():
        print(f"ID: {id_candidato}, Nome: {nome_candidato}, Número de Votação: {numero_votacao}, Partido: {partido}")

# Exemplo de uso
inserir_eleitor("Gabriel", "112233445566", "12345678901", True)
listar_eleitores()

inserir_candidato("Willian", "12345", "PL")
listar_candidatos()

# Fechar conexão
cursor.close()
conexao.close()

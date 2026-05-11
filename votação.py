import conexão_db
import os

cursor = conexão_db.conexao.cursor()

def validar_dados_eleitor():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== Abertura de Votação ===")

    titulo_eleitor = input("Título de Eleitor: ")
    cpf_4_digitos = input("4 primeiros dígitos do CPF: ")
    chave_acesso = input("Chave de Acesso: ")

# Consulta os dados no banco de dados
    cursor.execute("SELECT nome_eleitor, cpf, chave_acesso FROM eleitores WHERE titulo_eleitor = %s", (titulo_eleitor,))
    resultado = cursor.fetchone()

    if not resultado:
        print("\nO eleitor não foi localizado!")
        return False    
   
    nome_bd, cpf_bd, chave_bd = resultado

# *******COLOCAR A DESCRIPTOGRAFIA AQUI*******

# Validação dos quatro primeiros dígitos do CPF 
    if cpf_bd[:4] != cpf_4_digitos:
        print("\nCPF incorreto!")
        return False

# Validação da chave de acesso    
    if chave_bd != chave_acesso:
        print("\nChave de acesso incorreta!")
        return False
    
    print(f"\nIdentidade confirmada! Bem-vindo(a), {nome_bd}!")
    return True

from datetime import datetime

def criar_log():
    try:
        with open("logs.txt", "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        with open("logs.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Horário: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} --- Registro: Arquivo de Logs criado.\n")
            pass

def registrar_log(entrada):
    try:
        with open("logs.txt", "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        with open("logs.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(f"Horário: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} --- Registro: Arquivo de Logs criado.\n")
            pass

    with open("logs.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Horário: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} --- Registro: {entrada}\n")
    
def ler_log():
    try:
        with open("logs.txt", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            print(conteudo)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
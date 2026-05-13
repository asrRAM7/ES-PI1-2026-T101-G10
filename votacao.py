import conexao_db
import os
import criptografia
import time
import random
from datetime import datetime

cursor = conexao_db.conexao.cursor()

def validar_dados_eleitor(mesario):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Abertura de Votação ===")

    titulo_eleitor = input("Título de Eleitor: ")
    cpf_4_digitos = input("4 primeiros dígitos do CPF: ")
    chave_acesso = input("Chave de Acesso: ")

    titulo_criptografado = criptografia.criptografar(titulo_eleitor)
# Consulta os dados no banco de dados
    cursor.execute("SELECT nome_eleitor, cpf, chave_acesso, mesario, voto, id_eleitor FROM eleitores WHERE titulo_eleitor = %s", (titulo_criptografado,))
    resultado = cursor.fetchone()

    if not resultado:
        print("\nO eleitor não foi localizado!")
        input("\nPressione ENTER para continuar...")
        return False    

    chave_descriptogafada = criptografia.descriptografar(resultado[2], 7)
    cpf_descriptografado = criptografia.descriptografar(resultado[1], 4)
    id_eleitor = resultado[5]
# Validação dos quatro primeiros dígitos do CPF 
    if cpf_descriptografado != cpf_4_digitos:
        print("\nCPF incorreto!")
        input("\nPressione ENTER para continuar...")
        return False

# Validação da chave de acesso    
    if chave_descriptogafada != chave_acesso:
        print("\nChave de acesso incorreta!")
        input("\nPressione ENTER para continuar...")
        return False

    if mesario:
        if resultado[3] == 1:
            print(f"\n{resultado[0]} é mesário")
        else:
            print(f"\n{resultado[0]} não é mesário, portanto, não pode iniciar o sistema.")
            input("\nPressione ENTER para voltar...")
            return False
    
    print(f"\nIdentidade confirmada! Bem-vindo(a), {resultado[0]}!")
    if mesario:
        zerezima()
    if not mesario:
        if resultado[4] != None:
            print("\nVocê já votou! Não é possível votar novamente.")
            input("\nPressione ENTER para continuar...")
            return False
        else:
            votar(id_eleitor)
    time.sleep(0.25)
    return True

def zerezima():
    os.system('cls' if os.name == 'nt' else 'clear')
    total_passos = 30
    for i in range(31): 
        passo = i % (total_passos + 1)
        percentual = (passo / total_passos) * 100
        
        if i == 30:
            cor = "\033[32m" # Verde
        else:
            cor = "" # Cor padrão

        barra = "█" * passo + "-" * (total_passos - passo)
        
        print(f"\rFazendo a Zerézima: |{cor}{barra}\033[0m| {cor}{percentual:.2f}%\033[0m ", end="", flush=True)
        time.sleep(0.075)

    cursor.execute("UPDATE eleitores SET voto = NULL, protocolo_votacao = NULL, data_votacao = NULL")
    conexao_db.conexao.commit()

    cursor.execute("SELECT nome_eleitor, voto FROM eleitores")
    total_votos = cursor.fetchall()
    print()
    print(f"Votos zerados: {total_votos}")
    input("Pressione ENTER para iniciar votação... ")
    menu_votacao()

def menu_votacao():
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menu de Votação ===")
        print("1 - Votar\n2 - Encerrar Sistema de Votação")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                validar_dados_eleitor(False)
            case 2:
                print("\nEncerrando o sistema de votação...")
                time.sleep(0.25)
                return
            case _:
                print("Opção inválida.")

def votar(id):
    o = True
    while o:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Sistema de Votação ===")
        cursor.execute("SELECT nome_candidato, numero_votacao, partido FROM candidatos")
        candidatos = cursor.fetchall()
        print(f"\nCandidatos disponíveis (nome, número eleitoral, partido): {candidatos}")
        partido_voto = input("\nInforme o candidato (número eleitoral) que deseja votar: ")
        cursor.execute("SELECT nome_candidato, partido FROM candidatos WHERE numero_votacao = %s", (partido_voto,))
        candidato_selecionado = cursor.fetchone()
        o = votar2(candidato_selecionado, partido_voto, id)

def votar2(candidato_selecionado, partido_voto, id):
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Você escolheu votar em:", candidato_selecionado[0], "\nDo partido:", candidato_selecionado[1])
        print("\n[1] - Confirmar voto\n[2] - Cancelar voto")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor.execute("UPDATE eleitores SET voto = %s WHERE id_eleitor = %s", (partido_voto, id,))
                conexao_db.conexao.commit()
                input("\nVoto registrado com sucesso!")
                protocolo = protocolo_votacao(partido_voto)
                print(f"O seu protocolo de votação é: {protocolo}")
                data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE eleitores SET protocolo_votacao = %s, data_votacao = %s WHERE id_eleitor = %s", (criptografia.criptografar(protocolo), data, id,))
                conexao_db.conexao.commit()
                time.sleep(1.5)
                return False
            case 2:
                print("\nCancelando Voto...")
                time.sleep(0.25)
                return True
            case _:
                print("Opção inválida.")

def protocolo_votacao(candidato):
    afabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tamanho = 2
    resultado = "".join(random.choice(afabeto) for _ in range(tamanho))
    return "V"+str(resultado)+"26"+str(candidato)+str(random.randint(10000, 99999))

# 4h30min

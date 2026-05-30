import conexao_db
import os
import criptografia
import time
import random
from datetime import datetime
import auditoria

cursor = conexao_db.conexao.cursor()

def validar_dados_eleitor(mesario, encerrar):
    os.system('cls' if os.name == 'nt' else 'clear')
    if not encerrar:
        print("=== Abertura da Votação ===")
    else:
        print("=== Encerramento da Votação ===")

    titulo_eleitor = input("Título de Eleitor: ")
    cpf_4_digitos = input("4 primeiros dígitos do CPF: ")
    chave_acesso = input("Chave de Acesso: ")

    titulo_criptografado = criptografia.criptografar(titulo_eleitor)
# Consulta os dados no banco de dados
    cursor.execute("SELECT nome_eleitor, cpf, chave_acesso, mesario, votou, id_eleitor FROM eleitores WHERE titulo_eleitor = %s", (titulo_criptografado,))
    resultado = cursor.fetchone()

    if not resultado and not encerrar:
        print("\nO eleitor não foi localizado!")
        input("\nPressione ENTER para continuar...")
        return False
    if not resultado and encerrar:
        print("\nO mesário não foi localizado!")
        input("\nPressione ENTER para voltar...")
        return True

    chave_descriptogafada = criptografia.descriptografar(resultado[2], 7)
    cpf_descriptografado = criptografia.descriptografar(resultado[1], 4)
    id_eleitor = resultado[5]
# Validação dos quatro primeiros dígitos do CPF 
    if cpf_descriptografado != cpf_4_digitos:
        print("\nCPF incorreto!")
        input("\nPressione ENTER para continuar...")
        auditoria.registrar_log("ALERTA: Tentativa de acesso negado")
        return False

# Validação da chave de acesso    
    if chave_descriptogafada != chave_acesso:
        print("\nChave de acesso incorreta!")
        input("\nPressione ENTER para continuar...")
        auditoria.registrar_log("ALERTA: Tentativa de acesso negado")
        return False

    if mesario:
        if resultado[3] == 1:
            print(f"\n{resultado[0]} é mesário")
        else:
            print(f"\n{resultado[0]} não é mesário, portanto, não pode iniciar/encerrar o sistema.")
            input("\nPressione ENTER para voltar...")
            auditoria.registrar_log("ALERTA: Tentativa de acesso negado")
            return False
    
    print(f"\nIdentidade confirmada! Bem-vindo(a), {resultado[0]}!")
    if mesario and not encerrar:
        zerezima()
    if not mesario:
        if resultado[4] != None:
            print("\nVocê já votou! Não é possível votar novamente.")
            input("\nPressione ENTER para continuar...")
            auditoria.registrar_log("ALERTA: Tentativa de voto duplo")
            return False
        else:
            votar(id_eleitor)
    elif mesario and encerrar:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Encerramento da Votação ===\n   Você realmente deseja encerrar a votação?\n   [1] Sim\n   [2] Não")
        opcao = int(input("\n Escolha a opção: "))
        if opcao == 2:
            return True
        elif opcao == 1:
            chave = input("Digite a chave de acesso para confirmação: ")
            if chave == chave_descriptogafada:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Sistema de votaçao encerrado!")
                auditoria.registrar_log("ENCERRAMENTO: Votação finalizada com sucesso")
                time.sleep(0.5)
                return False
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

    cursor.execute("UPDATE eleitores SET votou = NULL")
    cursor.execute("DELETE FROM votos")
    conexao_db.conexao.commit()

    cursor.execute("SELECT nome_eleitor, votou FROM eleitores")
    total_votos = cursor.fetchall()
    print()
    print(f"Votos zerados: {total_votos}")
    auditoria.registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")
    input("Pressione ENTER para iniciar votação... ")
    menu_votacao()

def menu_votacao():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menu de Votação ===")
        print("1 - Votar\n2 - Encerrar Sistema de Votação\n3 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                validar_dados_eleitor(False, False)
            case 2:
                opcao = validar_dados_eleitor(True, True)
            case 3:
                print("Retornando ao menu principal...")
            case _:
                print("Opção inválida.")

def votar(id):
    o = True
    while o:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Sistema de Votação ===")
        partido_voto = input("\nInforme o candidato (número eleitoral) que deseja votar: ")
        cursor.execute("SELECT nome_candidato, partido FROM candidatos WHERE numero_votacao = %s", (partido_voto,))
        candidato_selecionado = cursor.fetchone()
        if candidato_selecionado is None:
            o = votar2(candidato_selecionado,partido_voto,id,nulo=True)
        else:
            o = votar2(candidato_selecionado, partido_voto, id, False)

def votar2(candidato_selecionado, partido_voto, id, nulo):
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        if not nulo:
            print("Você escolheu votar em:", candidato_selecionado[0], "\nDo partido:", candidato_selecionado[1])
            print("\n[1] - Confirmar voto\n[2] - Cancelar voto")
        else:
                print("Seu voto será registrado como Nulo, deseja confirmar?")
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
                if not nulo:
                    cursor.execute("UPDATE eleitores SET votou = %s WHERE id_eleitor = %s", (1, id,))
                    conexao_db.conexao.commit()
                    print("Voto registrado com sucesso!\n")
                    protocolo = protocolo_votacao(partido_voto,nulo=False)
                    print(f"O seu protocolo de votação é: {protocolo}")
                    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO votos (voto, protocolo_votacao, data_votacao) VALUES (%s, %s, %s)", (partido_voto, protocolo, data,))
                    conexao_db.conexao.commit()
                    auditoria.registrar_log("SUCESSO: Voto realizado com sucesso")
                    input("Pressione ENTER para voltar ")
                    return False
                else:
                    cursor.execute("UPDATE eleitores SET votou = %s WHERE id_eleitor = %s", (1, id,))
                    conexao_db.conexao.commit()
                    print("Voto registrado com sucesso!\n")
                    protocolo = protocolo_votacao(partido_voto,nulo=True)
                    print(f"O seu protocolo de votação é: {protocolo}")
                    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO votos (voto, protocolo_votacao, data_votacao) VALUES (00, %s, %s)", (protocolo, data,))
                    conexao_db.conexao.commit()
                    auditoria.registrar_log("SUCESSO: Voto realizado com sucesso")
                    input("Pressione ENTER para voltar ")
                    return False
            case 2:
                print("\nCancelando Voto...")
                time.sleep(0.25)
                return True
            case _:
                print("Opção inválida.")

def protocolo_votacao(candidato,nulo):
    afabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tamanho = 2
    resultado = "".join(random.choice(afabeto) for _ in range(tamanho))
    if not nulo:
        return "V"+str(resultado)+"26"+str(candidato)+str(random.randint(10000, 99999))
    elif nulo:
        return "V"+str(resultado)+"26"+"00"+str(random.randint(10000, 99999))

# 4h30min

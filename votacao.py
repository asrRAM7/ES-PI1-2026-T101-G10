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
        print("=" * 50)
        print(f"{'ABERTURA DA VOTAÇÃO':^50}")
        print("=" * 50)
    else:
        print("=" * 50)
        print(f"{'ENCERRAMENTO DA VOTAÇÃO':^50}")
        print("=" * 50)

    titulo_eleitor = input("Título de Eleitor: ")
    cpf_4_digitos = input("4 primeiros dígitos do CPF: ")
    chave_acesso = input("Chave de Acesso: ")
    titulo_eleitor = conexao_db.limpar_numeros(titulo_eleitor) 
    if len(titulo_eleitor) != 12:
        print("\nTítulo de Eleitor inválido!")
        input("\nPressione ENTER para continuar...")
        return False

    titulo_criptografado = criptografia.criptografar(titulo_eleitor)
# Consulta os dados no banco de dados
    cursor.execute("SELECT nome_eleitor, cpf, chave_acesso, mesario, votou, id_eleitor FROM eleitores WHERE titulo_eleitor = %s", (titulo_criptografado,))
    resultado = cursor.fetchone()

    if not resultado and not encerrar:
        print("\n\033[33mO eleitor não foi localizado!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        return False
    if not resultado and encerrar:
        print("\n\033[33mO mesário não foi localizado!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para voltar...")
        return True

    chave_descriptogafada = criptografia.descriptografar(resultado[2], 7)
    cpf_descriptografado = criptografia.descriptografar(resultado[1], 4)
    id_eleitor = resultado[5]
# Validação dos quatro primeiros dígitos do CPF 
    if cpf_descriptografado != cpf_4_digitos:
        print("\n\033[31mCPF incorreto!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        auditoria.registrar_log("\033[031mALERTA:\033[0m Tentativa de acesso negado")
        return False

# Validação da chave de acesso    
    if chave_descriptogafada != chave_acesso:
        print("\n\033[31mChave de acesso incorreta!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        auditoria.registrar_log("\033[31mALERTA:\033[0m Tentativa de acesso negado")
        return False

    if mesario:
        if resultado[3] == 1:
            print(f"\n{resultado[0]} é mesário")
        else:
            print(f"\n{resultado[0]} não é mesário, portanto, não pode iniciar/encerrar o sistema.")
            input("\nPressione \033[1m\033[37mENTER\033[0m para voltar...")
            auditoria.registrar_log("\033[31mALERTA:\033[0m Tentativa de acesso negado")
            return False
    
    print(f"\nIdentidade confirmada! Bem-vindo(a), \033[1m\033[37m{resultado[0]}!\033[0m")
    if mesario and not encerrar:
        zerezima()
    if not mesario:
        if resultado[4] != None:
            print("\n\033[33mVocê já votou!\033[0m Não é possível votar novamente.")
            input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            auditoria.registrar_log("\033[31mALERTA:\033[0m Tentativa de voto duplo")
            return False
        else:
            votar(id_eleitor)
    elif mesario and encerrar:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'ENCERRAMENTO DA VOTAÇÃO':^50}")
        print("=" * 50)
        print("   Você realmente deseja encerrar a votação?")
        print("   \033[1m\033[37m[1]\033[0m Sim\n   \033[1m\033[37m[2]\033[0m Não")
        opcao = int(input("\n Escolha a opção: "))
        if opcao == 2:
            return True
        elif opcao == 1:
            chave = input("Digite a chave de acesso para confirmação: ")
            if chave == chave_descriptogafada:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'VOTAÇÃO ENCERRADA':^50}")
                print("=" * 50)
                print("\n\033[32mSistema de votação encerrado com sucesso!\033[0m")
                print("\nVocê será redirecionado ao menu de Resultados e Auditoria.")
                auditoria.registrar_log("ENCERRAMENTO: Votação finalizada com sucesso")
                time.sleep(1.5)
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
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

    cursor.execute("SELECT nome_candidato, numero_votacao, partido FROM candidatos")
    candidatos = cursor.fetchall()
    print()
    print(f"\n{'─' * 55}")
    print(f"{'COMPROVAÇÃO DE URNA ZERADA':^55}")
    print(f"{'─' * 55}")
    print(f"  {'Candidato':<28} {'Número':^8} {'Votos':>6}")
    print(f"  {'─' * 46}")
    for (nome, numero, partido) in candidatos:
        print(f"  {nome:<28} {numero:^8} {'0':>6}")
    print(f"{'─' * 55}")
    print(f"\n\033[32mUrna zerada com sucesso! Todos os candidatos possuem 0 votos.\033[0m")
    auditoria.registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")
    input("\nPressione \033[1m\033[37mENTER\033[0m para iniciar votação... ")
    menu_votacao()

def validar_mesario():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 50)
    print(f"{'AUTENTICAÇÃO DE MESÁRIO':^50}")
    print("=" * 50)

    titulo_eleitor = input("Título de Eleitor: ")
    cpf_4_digitos = input("4 primeiros dígitos do CPF: ")
    chave_acesso = input("Chave de Acesso: ")

    titulo_eleitor = conexao_db.limpar_numeros(titulo_eleitor)
    if len(titulo_eleitor) != 12:
        print("\nTítulo de Eleitor inválido!")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        return False

    titulo_criptografado = criptografia.criptografar(titulo_eleitor)
    cursor.execute("SELECT nome_eleitor, cpf, chave_acesso, mesario FROM eleitores WHERE titulo_eleitor = %s", (titulo_criptografado,))
    resultado = cursor.fetchone()

    if not resultado:
        print("\n\033[33mMesário não localizado!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        return False

    chave_descriptografada = criptografia.descriptografar(resultado[2], 7)
    cpf_descriptografado = criptografia.descriptografar(resultado[1], 4)

    if cpf_descriptografado != cpf_4_digitos:
        print("\n\033[31mCPF incorreto!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        auditoria.registrar_log("\033[31mALERTA:\033[0m Tentativa de acesso negado")
        return False

    if chave_descriptografada != chave_acesso:
        print("\n\033[31mChave de acesso incorreta!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        auditoria.registrar_log("\033[31mALERTA:\033[0m Tentativa de acesso negado")
        return False

    if resultado[3] != 1:
        print(f"\n\033[31m{resultado[0]} não é mesário!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        auditoria.registrar_log("\033[31mALERTA:\033[0m Tentativa de acesso negado")
        return False

    print(f"\nIdentidade confirmada! Bem-vindo(a), \033[1m\033[37m{resultado[0]}!\033[0m")
    return True

def menu_votacao():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'MENU DE VOTAÇÃO':^50}")
        print("=" * 50)
        print("\033[1m\033[37m[1]\033[0m - Votar\n\033[1m\033[37m[2]\033[0m - Encerrar Sistema de Votação\n\033[1m\033[37m[3]\033[0m - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")
            continue
        match opcao:
            case 1:
                validar_dados_eleitor(False, False)
            case 2:
                resultado_encerramento = validar_dados_eleitor(True, True)
                if resultado_encerramento == False:
                    # Votação encerrada — sai do loop e retorna ao menu de votação (menus.py)
                    return
            case 3:
                print("Retornando ao menu principal...")
            case _:
                print("\033[33mOpção inválida.\033[0m")
                input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")

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
            print("\n\033[1m\033[37m[1]\033[0m - Confirmar voto\n\033[1m\033[37m[2]\033[0m - Cancelar voto")
        else:
                print("Seu voto será registrado como Nulo, deseja confirmar?")
                print("\n\033[1m\033[37m[1]\033[0m - Confirmar voto\n\033[1m\033[37m[2]\033[0m - Cancelar voto")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                if not nulo:
                    cursor.execute("UPDATE eleitores SET votou = %s WHERE id_eleitor = %s", (1, id,))
                    conexao_db.conexao.commit()
                    print("Voto registrado com sucesso!\n")
                    protocolo = protocolo_votacao(partido_voto, nulo=False)
                    protocolo_criptografado = criptografia.criptografar(protocolo)
                    print(f"O seu protocolo de votação é: \033[1m\033[37m{protocolo}\033[0m")
                    print(f"\033[90m(Guarde este protocolo — ele comprova que seu voto foi registrado)\033[0m")
                    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO votos (voto, protocolo_votacao, data_votacao) VALUES (%s, %s, %s)", (partido_voto, protocolo_criptografado, data,))
                    conexao_db.conexao.commit()
                    auditoria.registrar_log("SUCESSO: Voto realizado com sucesso")
                    input("\nPressione \033[1m\033[37mENTER\033[0m para voltar ")
                    return False
                else:
                    cursor.execute("UPDATE eleitores SET votou = %s WHERE id_eleitor = %s", (1, id,))
                    conexao_db.conexao.commit()
                    print("Voto registrado com sucesso!\n")
                    protocolo = protocolo_votacao(partido_voto, nulo=True)
                    protocolo_criptografado = criptografia.criptografar(protocolo)
                    print(f"O seu protocolo de votação é: \033[1m\033[37m{protocolo}\033[0m")
                    print(f"\033[90m(Guarde este protocolo — ele comprova que seu voto foi registrado)\033[0m")
                    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute("INSERT INTO votos (voto, protocolo_votacao, data_votacao) VALUES (00, %s, %s)", (protocolo_criptografado, data,))
                    conexao_db.conexao.commit()
                    auditoria.registrar_log("SUCESSO: Voto realizado com sucesso")
                    input("\nPressione \033[1m\033[37mENTER\033[0m para voltar ")
                    return False
            case 2:
                print("\nCancelando Voto...")
                time.sleep(0.25)
                return True
            case _:
                print("\033[33mOpção inválida.\33[0m")
                input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")

def protocolo_votacao(candidato,nulo):
    afabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tamanho = 2
    resultado = "".join(random.choice(afabeto) for _ in range(tamanho))
    if not nulo:
        return "V"+str(resultado)+"26"+str(candidato)+str(random.randint(10000, 99999))
    elif nulo:
        return "V"+str(resultado)+"26"+"00"+str(random.randint(10000, 99999))

# 4h30min

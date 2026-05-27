import conexao_db
import os
import criptografia
import time
import random
import auditoria
import mysql.connector


def validar_dados_eleitor(mesario, encerrar):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Abertura de Votação ===")

    titulo_eleitor = input("Título de Eleitor: ")
    cpf_4_digitos = input("4 primeiros dígitos do CPF: ")
    chave_acesso = input("Chave de Acesso: ")

    titulo_criptografado = criptografia.criptografar(titulo_eleitor)

    conexao_db.cursor.execute("SELECT nome_eleitor, cpf, chave_acesso, mesario, id_eleitor FROM eleitores WHERE titulo_eleitor = %s", (titulo_criptografado,))
    resultado = conexao_db.cursor.fetchone()

    if not resultado:
        print("\nO eleitor não foi localizado!")
        auditoria.registrar_log("ALERTA: Tentativa de acesso com título não cadastrado")
        input("\nPressione ENTER para continuar...")
        return False

    chave_descriptografada = criptografia.descriptografar(resultado[2], 7)
    cpf_descriptografado = criptografia.descriptografar(resultado[1], 4)
    id_eleitor = resultado[4]
    nome_eleitor = resultado[0]

    if cpf_descriptografado != cpf_4_digitos:
        print("\nCPF incorreto!")
        input("\nPressione ENTER para continuar...")
        auditoria.registrar_log(f"ALERTA: Acesso negado para '{nome_eleitor}' - CPF incorreto")
        return False

    if chave_descriptografada != chave_acesso:
        print("\nChave de acesso incorreta!")
        input("\nPressione ENTER para continuar...")
        auditoria.registrar_log(f"ALERTA: Acesso negado para '{nome_eleitor}' - Chave incorreta")
        return False

    if mesario:
        if resultado[3] == 1:
            print(f"\n{nome_eleitor} é mesário.")
        else:
            print(f"\n{nome_eleitor} não é mesário, portanto, não pode iniciar/encerrar o sistema.")
            input("\nPressione ENTER para voltar...")
            auditoria.registrar_log(f"ALERTA: '{nome_eleitor}' tentou acessar função de mesário sem permissão")
            return False

    print(f"\nIdentidade confirmada! Bem-vindo(a), {nome_eleitor}!")

    if mesario and not encerrar:
        zerezima(nome_eleitor)

    if not mesario:
        conexao_db.cursor.execute("SELECT id_voto FROM votos WHERE id_eleitor = %s", (id_eleitor,))
        ja_votou = conexao_db.cursor.fetchone()

        if ja_votou is not None:
            print("\nVocê já votou! Não é possível votar novamente.")
            auditoria.registrar_log(f"ALERTA: Eleitor '{nome_eleitor}' (ID {id_eleitor}) tentou votar novamente")
            input("\nPressione ENTER para continuar...")
            return False
        else:
            votar(id_eleitor, nome_eleitor)

    elif mesario and encerrar:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Encerramento da Votação ===")
        print("   Você realmente deseja encerrar a votação?")
        print("   [1] Sim\n   [2] Não")
        try:
            opcao = int(input("\n Escolha a opção: "))
        except ValueError:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")
            return True

        if opcao == 2:
            return True
        elif opcao == 1:
            chave = input("Digite a chave de acesso para confirmação: ")
            if chave == chave_descriptografada:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Sistema de votação encerrado!")
                auditoria.registrar_log(f"ENCERRAMENTO: Votação finalizada pelo mesário '{nome_eleitor}'")
                time.sleep(0.5)
                return False
            else:
                print("\nChave de confirmação incorreta. Encerramento cancelado.")
                input("\nPressione ENTER para continuar...")
                return True
        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")
            return True

    time.sleep(0.25)
    return True


def zerezima(nome_eleitor):
    os.system('cls' if os.name == 'nt' else 'clear')
    total_passos = 30
    for i in range(31):
        passo = i % (total_passos + 1)
        percentual = (passo / total_passos) * 100
        cor = "\033[32m" if i == 30 else ""
        barra = "█" * passo + "-" * (total_passos - passo)
        print(f"\rFazendo a Zerézima: |{cor}{barra}\033[0m| {cor}{percentual:.2f}%\033[0m ", end="", flush=True)
        time.sleep(0.075)

    conexao_db.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    conexao_db.cursor.execute("TRUNCATE TABLE votos")
    conexao_db.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conexao_db.conexao.commit()

    print("\n\nVotos zerados com sucesso!")
    auditoria.registrar_log(f"ABERTURA: Votação iniciada pelo mesário '{nome_eleitor}'. Total de votos zerado.")
    input("Pressione ENTER para iniciar a votação...")
    menu_votacao()


def menu_votacao():
    continuar = True
    while continuar:
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
                continuar = validar_dados_eleitor(True, True)
            case 3:
                continuar = False
            case _:
                print("Opção inválida.")
                input("Pressione ENTER para tentar novamente...")


def votar(id_eleitor, nome_eleitor):
    o = True
    while o:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Sistema de Votação ===")

        conexao_db.cursor.execute("SELECT id_candidato, nome_candidato, numero_votacao, partido FROM candidatos")
        candidatos = conexao_db.cursor.fetchall()
        if candidatos:
            print("\nCandidatos disponíveis:")
            for candidato in candidatos:
                print(f"  [{candidato[2]}] {candidato[1]} - {candidato[3]}")
        else:
            print("\nNenhum candidato cadastrado.")

        partido_voto = input("\nInforme o número eleitoral do candidato (0 para branco/nulo): ")

        if partido_voto == "0" or partido_voto.strip() == "":
            candidato_selecionado = (None, "Branco/Nulo", "Nulo")
            id_candidato = None
        else:
            conexao_db.cursor.execute("SELECT id_candidato, nome_candidato, partido FROM candidatos WHERE numero_votacao = %s", (partido_voto,))
            res = conexao_db.cursor.fetchone()
            if not res:
                print("\nCandidato não localizado! Seu voto será computado como NULO.")
                input("Pressione ENTER para confirmar o voto nulo...")
                candidato_selecionado = (None, "Nulo", "Nulo")
                id_candidato = None
            else:
                id_candidato = res[0]
                candidato_selecionado = (res[0], res[1], res[2])

        o = votar2(candidato_selecionado, id_eleitor, id_candidato, nome_eleitor)


def votar2(candidato_selecionado, id_eleitor, id_candidato, nome_eleitor):
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Você escolheu votar em: {candidato_selecionado[1]}")
        print(f"Do partido: {candidato_selecionado[2]}")
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
                protocolo = protocolo_votacao()
                protocolo_criptografado = criptografia.criptografar(protocolo)
                try:
                    sql = "INSERT INTO votos(id_eleitor, id_candidato, protocolo_votacao) VALUES (%s, %s, %s)"
                    conexao_db.cursor.execute(sql, (id_eleitor, id_candidato, protocolo_criptografado))
                    conexao_db.conexao.commit()
                    print("Voto registrado com sucesso!\n")
                    print(f"Seu protocolo de votação é: {protocolo}")
                    auditoria.registrar_log(f"SUCESSO: Voto registrado para o eleitor '{nome_eleitor}'")
                except mysql.connector.Error as err:
                    print(f"Erro ao salvar voto no banco: {err}")
                    conexao_db.conexao.rollback()
                input("\nPressione ENTER para voltar...")
                return False
            case 2:
                print("\nCancelando voto...")
                time.sleep(0.25)
                return True
            case _:
                print("Opção inválida.")


def protocolo_votacao():
    # Gera protocolo fixo de 12 caracteres: V + 2 letras + 26 + 7 dígitos = 12
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letras = "".join(random.choice(alfabeto) for _ in range(2))
    numeros = str(random.randint(1000000, 9999999))
    return "V" + letras + "26" + numeros

import os
import conexão_db

def main_menu():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Módulos do Sistema de Votação ===")
        print("1 - Módulo de Gerenciamento\n2 - Módulo de Votação\n3 - Encerrar Sistema")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                menu_gerenciamento()
            case 2:
                menu_votacao()
            case 3:
                conexão_db.fechar_conexao()
                print("Encerrando sistema...")
            case _:
                print("Opção inválida.")

def menu_gerenciamento():
    opcao = 0
    while opcao != 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Menu do Módulo de Gerenciamento ===")
        print("1 - Cadastrar Novo Eleitor\n2 - Cadastrar Novo Candidato\n3 - Buscas Eleitor\n4 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                # ****** FAZER VALIDAÇÃO PARA NÃO PODER COLOCAR O MESMO CPF ***********
                print("\n=== Cadastramento de Eleitor ===")
                nome = input("Nome Completo: ")
                titulo = input("Título de Eleitor: ")
                cpf = input("CPF: ")
                mesario = int(input("É mesário? (1-Sim / 0-Não): "))
                chave_acesso=0
                conexão_db.inserir_eleitor(nome, titulo, cpf, mesario, chave_acesso)
                input("\nPressione ENTER para continuar...")
            case 2:
                print("\n=== Cadastramento de Candidato ===")
                input("\nPressione ENTER para continuar...")
            case 3:
                print("\n=== Busca de Eleitor ===")
                entrada = input("Digite o CPF ou Título: ")
                conexão_db.busca_eleitor(entrada)
                input("\nPressione ENTER para continuar...")
            case 4:
                print("Retornando ao menu principal...")
            case _:
                print("Opção inválida.")

def menu_votacao():
    opcao = 0
    while opcao != 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Menu do Módulo de Votação ===")
        print("1 - Abrir Sistema de Votação\n2 - Auditoria do Sistema de Votação\n3 - Resultado da Votação\n4 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                print("\n=== Sistema de Votação ===")
                input("\nPressione ENTER para continuar...")
            case 2:
                menu_auditoria()
            case 3:
                menu_resultados()
            case 4:
                print("Retornando ao menu principal...")
            case _:
                print("Opção inválida.")

def menu_resultados():
    opcao = 0
    while opcao != 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Resultados da Votação ===")
        print("1 - Boletim de Urna\n2 - Estatística de Comparecimento\n3 - Votos por Partido\n4 - Validação da Integridade\n5 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                print("\n=== Boletim de Urna ===")
                input("\nPressione ENTER para continuar...")
            case 2:
                print("\n=== Estatística de Comparecimento ===")
                input("\nPressione ENTER para continuar...")
            case 3:
                print("\n=== Votos por Partido ===")
                input("\nPressione ENTER para continuar...")
            case 4:
                print("\n=== Validação da Integridade ===")
                input("\nPressione ENTER para continuar...")
            case 5:
                print("Retornando...")
            case _:
                print("Opção inválida.")

def menu_auditoria():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== Auditoria do Sistema de Votação ===")
        print("1 - Exibir Protocolos de Votação\n2 - Exibir Logs de Ocorrências\n3 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                print("\n=== Protocolos de Votação ===")
                input("\nPressione ENTER para continuar...")
            case 2:
                print("\n=== Logs de Ocorrências ===")
                input("\nPressione ENTER para continuar...")
            case 3:
                print("Retornando...")
            case _:
                print("Opção Inválida.")

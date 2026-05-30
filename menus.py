import os
import conexao_db
import votacao
import auditoria
import time

def main_menu():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Módulos do Sistema de Votação ===")
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
                print("Encerrando sistema...")
            case _:
                print("Opção inválida.")

def menu_gerenciamento():
    opcao = 0
    while opcao != 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menu do Módulo de Gerenciamento ===")
        print("1 - Cadastrar Novo Eleitor\n2 - Cadastrar Novo Candidato\n3 - Buscar Eleitor\n4 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                # ****** FAZER VALIDAÇÃO PARA NÃO PODER COLOCAR O MESMO CPF, ACHO QUE DA PRA FAZER ISSO NA FUNÇÃO INSERIR_ELEITOR***********
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Cadastramento de Eleitor ===")
                conexao_db.inserir_eleitor()
                input("\nPressione ENTER para continuar...")
            case 2:
                print("\n=== Cadastramento de Candidato ===")
                nome_candidato = input("Nome do Candidato: ")
                while True:
                    try:
                        numero_votacao = int(input("Número de Votação: "))
                        break
                    except ValueError:
                        print("Número inválido. Digite apenas números.")
                partido = input("Partido: ")
                conexao_db.inserir_candidato(nome_candidato, numero_votacao, partido)
                input("\nPressione ENTER para continuar...")
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Busca de Eleitor ===")
                entrada = input("Digite o CPF ou Título: ")
                conexao_db.busca_eleitor(entrada)
                input("\nPressione ENTER para continuar...")
            case 4:
                print("Retornando ao menu principal...")
            case _:
                print("Opção inválida.")

def menu_votacao():
    opcao = 0
    while opcao != 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Menu do Módulo de Votação ===")
        print("1 - Abrir Sistema de Votação\n2 - Auditoria do Sistema de Votação\n3 - Resultado da Votação\n4 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                votacao.validar_dados_eleitor(True, False)
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
        print("=== Resultados da Votação ===")
        print("1 - Boletim de Urna\n2 - Estatística de Comparecimento\n3 - Votos por Partido\n4 - Verificação de Integridade\n5 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=== Boletim de Urna ===")
                conexao_db.boletim_urna()
                input("\nPressione ENTER para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=== Estatística de Comparecimento ===")
                conexao_db.estatistica_comparecimento()
                input("\nPressione ENTER para continuar...")
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=== Votos por Partido ===")
                conexao_db.votos_por_partido()
                input("\nPressione ENTER para continuar...")
            case 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=== Verificação de Integridade ===")
                conexao_db.validar_integridade()
                input("\nPressione ENTER para continuar...")
            case 5:
                print("Retornando...")
            case _:
                print("Opção inválida.")

def menu_auditoria():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Auditoria do Sistema de Votação ===")
        print("1 - Exibir Protocolos de Votação\n2 - Exibir Logs de Ocorrências\n3 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=== Protocolos de Votação ===")
                conexao_db.listar_protocolos()
                input("\nPressione ENTER para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Logs de Ocorrências ===\n")
                auditoria.ler_log()
                input("\nPressione ENTER para voltar...")
            case 3:
                print("Retornando...")
            case _:
                print("Opção Inválida.")

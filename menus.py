import os
import conexao_db
import votacao
import auditoria


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
                votacao.menu_votacao()
            case 3:
                conexao_db.fechar_conexao()
                print("Encerrando sistema...")
            case _:
                print("Opção inválida.")
                input("Pressione ENTER para tentar novamente...")


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
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Cadastramento de Eleitor ===")
                nome = input("Nome Completo: ")
                titulo = input("Título de Eleitor: ")
                titulo_limpo = conexao_db.limpar_numeros(titulo)
                if conexao_db.validar_titulo(titulo_limpo) == 0:
                    print("Erro: Título de Eleitor inválido!")
                    input("\nPressione ENTER para continuar...")
                    continue
                cpf = input("CPF: ")
                cpf_limpo = conexao_db.limpar_numeros(cpf)
                if conexao_db.validar_cpf(cpf_limpo) == 0:
                    print("Erro: CPF inválido!")
                    input("\nPressione ENTER para continuar...")
                    continue
                while True:
                    try:
                        mesario = int(input("É mesário? (1-Sim / 0-Não): "))
                        if mesario in (0, 1):
                            break
                        print("Digite apenas 1 para Sim ou 0 para Não.")
                    except ValueError:
                        print("Entrada inválida. Digite 1 ou 0.")
                conexao_db.inserir_eleitor(nome, titulo_limpo, cpf_limpo, mesario, 0)
                input("\nPressione ENTER para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Cadastramento de Candidato ===")
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
                entrada = input("Digite o CPF ou Título de Eleitor: ")
                conexao_db.busca_eleitor(entrada)
                input("\nPressione ENTER para continuar...")

            case 4:
                print("Retornando ao menu principal...")

            case _:
                print("Opção inválida.")
                input("Pressione ENTER para tentar novamente...")


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
                input("Pressione ENTER para tentar novamente...")


def menu_resultados():
    opcao = 0
    while opcao != 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Resultados da Votação ===")
        print("1 - Boletim de Urna\n2 - Estatística de Comparecimento\n3 - Votos por Partido\n4 - Protocolos de Votação\n5 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Boletim de Urna ===")
                conexao_db.boletim_urna()
                input("\nPressione ENTER para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Estatística de Comparecimento ===")
                conexao_db.estatistica_comparecimento()
                input("\nPressione ENTER para continuar...")
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Votos por Partido ===")
                conexao_db.votos_por_partido()
                input("\nPressione ENTER para continuar...")
            case 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Protocolos de Votação ===")
                conexao_db.listar_protocolos()
                input("\nPressione ENTER para continuar...")
            case 5:
                print("Retornando...")
            case _:
                print("Opção inválida.")
                input("Pressione ENTER para tentar novamente...")


def menu_auditoria():
    opcao = 0
    while opcao != 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Auditoria do Sistema de Votação ===")
        print("1 - Exibir Logs de Ocorrências\n2 - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("Opção inválida. Por favor, informe um número.")
            input("Pressione ENTER para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Logs de Ocorrências ===\n")
                auditoria.ler_log()
                input("\nPressione ENTER para voltar...")
            case 2:
                print("Retornando...")
            case _:
                print("Opção Inválida.")
                input("Pressione ENTER para tentar novamente...")

import os
import conexao_db
import votacao
import auditoria
import time

def main_menu():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'MÓDULOS DO SISTEMA DE VOTAÇÃO':^50}")
        print("=" * 50)
        print("\033[1m\033[37m[1]\033[0m Módulo de Gerenciamento\n\033[1m\033[37m[2]\033[0m Módulo de Votação\n\033[1m\033[37m[3]\033[0m Encerrar Sistema")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")            
            continue
        match opcao:
            case 1:
                menu_gerenciamento()
            case 2:
                menu_votacao()
            case 3:
                print("Encerrando sistema...")
            case _:
                print("\033[33mOpção inválida.\033[0m")
                input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")

def menu_gerenciamento():
    opcao = 0
    while opcao != 7:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'MENU DO MÓDULO DO GERENCIAMENTO':^50}")
        print("=" * 50)
        print("\033[1m\033[37m[1]\033[0m - Cadastrar Novo Eleitor\n\033[1m\033[37m[2]\033[0m - Cadastrar Novo Candidato\n\033[1m\033[37m[3]\033[0m - Buscar Eleitor\n\033[1m\033[37m[4]\033[0m - Buscar Candidato\n\033[1m\033[37m[5]\033[0m - Listar Eleitores\n\033[1m\033[37m[6]\033[0m - Listar Candidatos\n\033[1m\033[37m[7]\033[0m - Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'CADASTRO DE ELEITOR':^50}")
                print("=" * 50)
                conexao_db.inserir_eleitor()
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'CADASTRAMENTO DE CANDIDATO':^50}")
                print("=" * 50)
                nome_candidato = input("Nome do Candidato: ")
                while True:
                    try:
                        numero_votacao = int(input("Número de Votação: "))
                        break
                    except ValueError:
                        print("\033[33mNúmero inválido.\033[0m Digite apenas números.")
                partido = input("Partido: ")
                conexao_db.inserir_candidato(nome_candidato, numero_votacao, partido)
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'BUSCA DE ELEITOR':^50}")
                print("=" * 50)
                entrada = input("Digite o CPF ou Título: ")
                conexao_db.busca_eleitor(entrada)
            case 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'BUSCA DE CANDIDATO':^50}")
                print("=" * 50)
                numero = input("Digite o número de votação: ")
                conexao_db.busca_candidato(numero)
            case 5:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'LISTA DE ELEITORES':^50}")
                print("=" * 50)
                if votacao.validar_mesario():
                    conexao_db.listar_eleitores()
                    input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 6:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'LISTA DE CANDIDATOS':^50}")
                print("=" * 50)
                if votacao.validar_mesario():
                    conexao_db.listar_candidatos()
                    input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 7:
                print("Retornando ao menu principal...")
            case _:
                print("\033[33mOpção inválida.\033[0m")
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")

def menu_votacao():
    opcao = 0
    while opcao != 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'MENU DO MÓDULO DE VOTAÇÃO':^50}")
        print("=" * 50)
        print("\033[1m\033[37m[1]\033[0m Abrir Sistema de Votação\n\033[1m\033[37m[2]\033[0m Auditoria do Sistema de Votação\n\033[1m\033[37m[3]\033[0m Resultado da Votação\n\033[1m\033[37m[4]\033[0m Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")            
            continue
        match opcao:
            case 1:
                votacao.validar_dados_eleitor(True, False)
                # Após encerramento da votação, o fluxo retorna aqui
                # com Auditoria e Resultados disponíveis no menu
            case 2:
                menu_auditoria()
            case 3:
                menu_resultados()
            case 4:
                print("Retornando ao menu principal...")
            case _:
                print("\033[33mOpção inválida.\033[0m")
                input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")

def menu_resultados():
    opcao = 0
    while opcao != 5:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'RESULTADOS DA VOTAÇÃO':^50}")
        print("=" * 50)
        print("\033[1m\033[37m[1]\033[0m Boletim de Urna\n\033[1m\033[37m[2]\033[0m Estatística de Comparecimento\n\033[1m\033[37m[3]\033[0m Votos por Partido\n\033[1m\033[37m[4]\033[0m Verificação de Integridade\n\033[1m\033[37m[5]\033[0m Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'BOLETIM DE URNA':^50}")
                print("=" * 50)
                conexao_db.boletim_urna()
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'ESTATÍSTICA DE COMPARECIMENTO':^50}")
                print("=" * 50)
                conexao_db.estatistica_comparecimento()
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'VOTOS POR PARTIDO':^50}")
                print("=" * 50)
                conexao_db.votos_por_partido()
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'VALIDAÇÃO DE INTEGRIDADE':^50}")
                print("=" * 50)
                conexao_db.validar_integridade()
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 5:
                print("Retornando...")
            case _:
                print("\033[33mOpção inválida.\033[0m")
                input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")

def menu_auditoria():
    opcao = 0
    while opcao != 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print(f"{'AUDITORIA DO SISTEMA DE VOTAÇÃO':^50}")
        print("=" * 50)
        print("\033[1m\033[37m[1]\033[0m Exibir Protocolos de Votação\n\033[1m\033[37m[2]\033[0m Exibir Logs de Ocorrências\n\033[1m\033[37m[3]\033[0m Retornar")
        try:
            opcao = int(input("Informe a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m Por favor, informe um número.")
            input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")
            continue
        match opcao:
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'PROTOCOLOS DE VOTAÇÃO':^50}")
                print("=" * 50)
                conexao_db.listar_protocolos()
                input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 50)
                print(f"{'LOGS DE OCORRÊNCIA':^50}")
                print("=" * 50)
                auditoria.ler_log()
                input("\nPressione \033[1m\033[37mENTER\033[0m para voltar...")
            case 3:
                print("Retornando...")
            case _:
                print("\033[33mOpção inválida.\033[0m")
                input("Pressione \033[1m\033[37mENTER\033[0m para tentar novamente...")
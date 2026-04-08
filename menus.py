import os

def main_menu():
    os.system('cls')
    print("\n=== Módulos do Sistema de Votação ===")
    print("1 - Módulo de Gerenciamento\n2 - Módulo de Votação\n3 - Encerrar Sistema")
    opcao = int(input("Informe a opção escolhida: "))
    match opcao:
        case 1:
            menu_gerenciamento()
        case 2:
            menu_votacao()
        case 3:
            print("Encerrando sistema...")
        case _:
            print("Opção inválida.")
    return opcao

def menu_gerenciamento():
    os.system('cls')
    print("\n=== Menu do Módulo de Gerenciamento ===")
    print("1 - Cadastrar Novo Eleitor\n2 - Cadastrar Novo Candidato\n3 - Retornar")
    opcao = int(input("Informe a opção escolhida: "))
    match opcao:
        case 1:
            print("\n=== Cadastramento de Eleitor ===")
        case 2:
            print("\n=== Cadastramento de Candidato ===")
        case 3:
            print("Retornando ao menu principal...")
            main_menu()
        case _:
            print("Opção inválida.")

def menu_votacao():
    os.system('cls')
    print("\n=== Menu do Módulo de Votação ===")
    print("1 - Abrir Sistema de Votação\n2 - Auditoria do Sistema de Votação\n3 - Resultado da Votação\n4 - Retornar")
    opcao = int(input("Informe a opção escolhida: "))
    match opcao:
        case 1:
            print("\n=== Sistema de Votação ===")
        case 2:
            menu_auditoria()
        case 3:
            menu_resultados()
        case 4:
            print("Retornando ao menu principal...")
            main_menu()
        case _:
            print("Opção inválida.")

def menu_resultados():
    os.system('cls')
    print("\n=== Resultados da Votação ===")
    print("1 - Boletim de Urna\n2 - Estatística de Comparecimento\n3 - Votos por Partido\n4 - Validação da Integridade\n5 - Retornar")
    opcao = int(input("Informe a opção escolhida: "))
    match opcao:
        case 1:
            print("\n=== Boletim de Urna ===")
        case 2:
            print("\n=== Estatística de Comparecimento ===")
        case 3:
            print("\n=== Votos por Partido ===")
        case 4:
            print("\n=== Validação da Integridade ===")
        case 5:
            print("Retornando...")
            menu_votacao()
        case _:
            print("Opção inválida.")

def menu_auditoria():
    os.system('cls')
    print("\n=== Auditoria do Sistema de Votação ===")
    print("1 - Exibir Protocolos de Votação\n2 - Exibir Logs de Ocorrências\n3 - Retornar")
    opcao = int(input("Informe a opção escolhida: "))
    match opcao:
        case 1:
            print("\n=== Protocolos de Votação ===")
        case 2:
            print("\n=== Logs de Ocorrências ===")
        case 3:
            print("Retornando...")
            menu_votacao()
        case _:
            print("Opção Inválida.")
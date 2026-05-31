import mysql.connector
import random
import criptografia

# Conexão com o banco
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Alexander0202*',
    database='eleicao_db',
)
cursor = conexao.cursor()

# ---------- Inserir um novo usuário ----------
def inserir_eleitor():
# Verificação CPF e Título
    nome_eleitor = input("Nome Completo: ")
    titulo_eleitor = input("Título de Eleitor: ")
    titulo_eleitor = limpar_numeros(titulo_eleitor)
    if validar_titulo(titulo_eleitor) == 0:
        print("\033[31mErro:\033[0m Título de Eleitor inválido!")
        return
    
    cpf = input("CPF: ")
    cpf = limpar_numeros(cpf)
    if validar_cpf(cpf) == 0:
        print("\033[31mErro:\033[0m CPF inválido!")
        return
    mesario = int(input("É mesário? (\033[1m\033[37m[1]\033[0m - Sim / \033[1m\033[37m[0]\033[0m - Não): "))

# Passou nas duas verificações:
    chave_acesso = gerar_chave(nome_eleitor)
# Criptografar os dados antes de inserir no banco de dados
    chave_criptografada = criptografia.criptografar(chave_acesso)
    cpf_criptografado = criptografia.criptografar(cpf)
    titulo_criptografado = criptografia.criptografar(titulo_eleitor)
    try:
        if not conexao.is_connected():
            conexao.reconnect(attempts=3, delay=1)
        sql = "INSERT INTO eleitores (nome_eleitor, titulo_eleitor, cpf, mesario, chave_acesso) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome_eleitor, titulo_criptografado, cpf_criptografado, mesario, chave_criptografada)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"\033[32mEleitor inserido com Sucesso!\033[0m")
        print(f"Chave de Acesso Gerada (Anote ela para não perder): \033[1m\033[37m{chave_acesso}\033[0m")
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            print(f"\n\033[31m[ERRO]\033[0m Já existe um eleitor cadastrado com este CPF ou Título de Eleitor!")
        else:
            print(f"\033[31mErro ao inserir no banco:\033[0m {erro}")
            conexao.rollback()

def inserir_candidato(nome_candidato, numero_votacao, partido):
    try:
        if not conexao.is_connected():
            conexao.reconnect(attempts=3, delay=1)
        sql = "INSERT INTO candidatos (nome_candidato, numero_votacao, partido) VALUES (%s, %s, %s)"
        valores = (nome_candidato, numero_votacao, partido)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"\nCandidato '{nome_candidato}' cadastrado com sucesso! ID: \033[1m\033[37m{cursor.lastrowid}\033[0m")
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            print(f"\n\033[31m[ERRO]\033[0m Já existe um candidato com este número de votação!")
        else:
            print(f"\033[31mErro ao inserir candidato:\033[0m \033[1m\033[37m{erro}\033[0m")
            conexao.rollback()

# ---------- Validação de CPF ----------
def validar_cpf(cpf):
    if len(cpf) != 11:
        return 0  
    if cpf == cpf[0] * 11:
        return 0  
# Cálculo do primeiro dígito verificador
    soma1 = 0
    multiplicador = 10
    for i in range(9):
        soma1 = soma1 + (int(cpf[i]) * multiplicador)
        multiplicador = multiplicador - 1
    resto1 = soma1 % 11
    if resto1 < 2:
        verificador1 = 0
    else:
        verificador1 = 11 - resto1
    if int(cpf[9]) != verificador1:
        return 0
# Cálculo do segundo dígito verificador
    soma2 = 0
    multiplicador = 11
    for i in range(10):
        soma2 = soma2 + (int(cpf[i]) * multiplicador)
        multiplicador = multiplicador - 1
    resto2 = soma2 % 11
    if resto2 < 2:
        verificador2 = 0
    else:
        verificador2 = 11 - resto2
    if int(cpf[10]) == verificador2:
        return 1
    else:
        return 0
        
# ---------- Validação do Título ---------- ******* VALIDAR CORRETAMENTE *********
def validar_titulo(titulo):
    if len(titulo) != 12 or not titulo.isdigit():
        return 0
    sequencial = titulo[:8]
    uf = titulo[8:10]
    digito_verificador = titulo[10:] #dv
    soma = 0
    peso = [2, 3, 4, 5, 6, 7, 8, 9]

    # Cálculo do dígito verificador 1
    for i in range(8):
        soma += int(sequencial[i]) * peso[i]
    resto = soma % 11

    if resto == 10:
        dv1 = 0
    elif resto == 0 and uf in ['01', '02']:
        dv1 = 1
    else:
        dv1 = resto

    # Cálculo do dígito verificador 2
    soma2 = (int(uf[0])*7)+(int(uf[1])*8)+(dv1*9)
    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and uf in ['01', '02']:
        dv2 = 1
    else:
        dv2 = resto2

    dv_results = f"{dv1}{dv2}"
    if dv_results == digito_verificador:
        return 1 # título valido
    else:
        return 0 # título inválido
    
# ---------- Gerar Chave ----------
def gerar_chave(nome):
    nome = limpar_entrada(nome)
    parte_do_nome = nome[0] + nome[1] + nome[2]
    partes_nome = nome.split()
    if len (partes_nome) >= 2:
        primeiro_nome = partes_nome[0]
        segundo_nome = partes_nome[1]
        parte_do_nome = primeiro_nome[:2] + segundo_nome[0]
    else:
        parte_do_nome = nome[:3]
    numero_aleatorio = random.randint(1000, 9999)
    chave = str(parte_do_nome).upper() + str(numero_aleatorio)
    return chave

# Funcão para limpar acentos de uma entrada
def limpar_entrada(entrada):
    entrada = entrada.upper()

    com_acento = "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ"
    sem_acento = "AAAAAEEEEIIIIOOOOOOUUUUCN"
    
    for i in range(len(com_acento)):
        entrada = entrada.replace(com_acento[i], sem_acento[i])
    
    return entrada

# Função para limpar pontuação
def limpar_numeros(entrada):
    return ''.join(c for c in entrada if c.isdigit())


# ---------- Buscar todos os usuários ----------
def listar_eleitores():
    cursor.execute("SELECT nome_eleitor, titulo_eleitor, cpf, mesario FROM eleitores")
    for (nome_eleitor, titulo_eleitor, cpf, mesario) in cursor.fetchall():
        mesario_str = "Sim" if mesario == 1 else "Não"
        titulo_desc = criptografia.descriptografar(titulo_eleitor, 12)
        cpf_desc = criptografia.descriptografar(cpf, 11)
        print(f"Nome: {nome_eleitor}, Título de Eleitor: {titulo_desc}, CPF: {cpf_desc}, Mesário: {mesario_str}")
def listar_candidatos():
    cursor.execute("SELECT nome_candidato, numero_votacao, partido FROM candidatos")
    for (nome_candidato, numero_votacao, partido) in cursor.fetchall():
        print(f"Nome: {nome_candidato}, Número de Votação: {numero_votacao}, Partido: {partido}")

# ---------- Busca específica de eleitor ----------
def busca_eleitor(entrada):
    entrada = limpar_numeros(entrada)
    if len(entrada) not in (11, 12):
        print("\nEntrada inválida! Digite um CPF (11 dígitos) ou Título de Eleitor (12 dígitos).")
        return
    entrada = criptografia.criptografar(entrada)
    comando = "SELECT nome_eleitor, cpf, titulo_eleitor, chave_acesso, id_eleitor FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"
    cursor.execute(comando, (entrada, entrada))
    resultado = cursor.fetchone()
    if resultado:
        print(f"\nResultado encontrado:")
        print(f"Nome: {resultado[0]}")
        print(f"CPF: {criptografia.descriptografar(resultado[1], 11)}")
        print(f"Título de Eleitor: {criptografia.descriptografar(resultado[2], 12)}")
        print(f"Chave de Acesso: {criptografia.descriptografar(resultado[3], 7)}")
        id_eleitor = resultado[4]
        print(f"\n\033[1m\033[37m[1]\033[0m - Editar Eleitor")
        print(f"\033[1m\033[37m[2]\033[0m - Excluir Eleitor")
        print(f"\033[1m\033[37m[3]\033[0m - Voltar")
        try:
            opcao = int(input("\nInforme a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m")
            return
        if opcao == 1:
            import votacao
            if votacao.validar_mesario():
                editar_eleitor(id_eleitor)
        elif opcao == 2:
            import votacao
            if votacao.validar_mesario():
                excluir_eleitor(id_eleitor)
    else:
        print("\n\033[33mEleitor não localizado\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")

def editar_eleitor(id_eleitor):
    print("\nDeixe em branco para manter o valor atual.")
    nome = input("Novo nome: ")
    titulo = input("Novo Título de Eleitor: ")
    titulo = limpar_numeros(titulo)
    cpf = input("Novo CPF: ")
    cpf = limpar_numeros(cpf)

    if titulo and validar_titulo(titulo) == 0:
        print("\033[31mErro:\033[0m Título inválido!")
        return
    if cpf and validar_cpf(cpf) == 0:
        print("\033[31mErro:\033[0m CPF inválido!")
        return

    campos = []
    valores = []
    if nome:
        campos.append("nome_eleitor = %s")
        valores.append(nome)
    if titulo:
        campos.append("titulo_eleitor = %s")
        valores.append(criptografia.criptografar(titulo))
    if cpf:
        campos.append("cpf = %s")
        valores.append(criptografia.criptografar(cpf))

    if not campos:
        print("\nNenhuma alteração realizada.")
        return

    valores.append(id_eleitor)
    sql = f"UPDATE eleitores SET {', '.join(campos)} WHERE id_eleitor = %s"
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print("\n\033[32mEleitor atualizado com sucesso!\033[0m")
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            print(f"\n\033[31m[ERRO]\033[0m CPF ou Título já cadastrado para outro eleitor!")
        else:
            print(f"\033[31mErro ao atualizar:\033[0m {erro}")
            conexao.rollback()

def excluir_eleitor(id_eleitor):
    print("\n\033[33mAtenção:\033[0m Esta ação é irreversível!")
    confirmar = input("Digite \033[1m\033[37mSIM\033[0m para confirmar a exclusão: ")
    if confirmar.strip().upper() != "SIM":
        print("\nExclusão cancelada.")
        return
    try:
        cursor.execute("DELETE FROM eleitores WHERE id_eleitor = %s", (id_eleitor,))
        conexao.commit()
        print("\n\033[32mEleitor excluído com sucesso!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
    except mysql.connector.Error as erro:
        print(f"\033[31mErro ao excluir:\033[0m {erro}")
        conexao.rollback()


def busca_candidato(numero):
    try:
        numero = int(numero)
    except ValueError:
        print("\nNúmero de votação inválido!")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
        return
    cursor.execute("SELECT id_candidato, nome_candidato, numero_votacao, partido FROM candidatos WHERE numero_votacao = %s", (numero,))
    resultado = cursor.fetchone()
    if resultado:
        print(f"\nResultado encontrado:")
        print(f"Nome     : {resultado[1]}")
        print(f"Número   : {resultado[2]}")
        print(f"Partido  : {resultado[3]}")
        id_candidato = resultado[0]
        print("\n\033[1m\033[37m[1]\033[0m - Editar Candidato")
        print("\033[1m\033[37m[2]\033[0m - Excluir Candidato")
        print("\033[1m\033[37m[3]\033[0m - Voltar")
        try:
            opcao = int(input("\nInforme a opção escolhida: "))
        except ValueError:
            print("\033[33mOpção inválida.\033[0m")
            return
        if opcao == 1:
            import votacao
            if votacao.validar_mesario():
                editar_candidato(id_candidato)
        elif opcao == 2:
            import votacao
            if votacao.validar_mesario():
                excluir_candidato(id_candidato)
    else:
        print("\n\033[33mCandidato não localizado\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")

def editar_candidato(id_candidato):
    print("\nDeixe em branco para manter o valor atual.")
    nome = input("Novo nome: ")
    numero_str = input("Novo número de votação: ").strip()
    partido = input("Novo partido: ")

    campos = []
    valores = []
    if nome:
        campos.append("nome_candidato = %s")
        valores.append(nome)
    if numero_str:
        try:
            numero = int(numero_str)
            campos.append("numero_votacao = %s")
            valores.append(numero)
        except ValueError:
            print("\033[31mErro:\033[0m Número de votação inválido!")
            return
    if partido:
        campos.append("partido = %s")
        valores.append(partido)

    if not campos:
        print("\nNenhuma alteração realizada.")
        return

    valores.append(id_candidato)
    sql = f"UPDATE candidatos SET {', '.join(campos)} WHERE id_candidato = %s"
    try:
        cursor.execute(sql, valores)
        conexao.commit()
        print("\n\033[32mCandidato atualizado com sucesso!\033[0m")
    except mysql.connector.Error as erro:
        if erro.errno == 1062:
            print(f"\n\033[31m[ERRO]\033[0m Já existe um candidato com este número de votação!")
        else:
            print(f"\033[31mErro ao atualizar:\033[0m {erro}")
            conexao.rollback()

def excluir_candidato(id_candidato):
    print("\n\033[33mAtenção:\033[0m Esta ação é irreversível!")
    confirmar = input("Digite \033[1m\033[37mSIM\033[0m para confirmar a exclusão: ")
    if confirmar.strip().upper() != "SIM":
        print("\nExclusão cancelada.")
        return
    try:
        cursor.execute("DELETE FROM candidatos WHERE id_candidato = %s", (id_candidato,))
        conexao.commit()
        print("\n\033[32mCandidato excluído com sucesso!\033[0m")
        input("\nPressione \033[1m\033[37mENTER\033[0m para continuar...")
    except mysql.connector.Error as erro:
        print(f"\033[31mErro ao excluir:\033[0m {erro}")
        conexao.rollback()

def boletim_urna():
    cursor.execute("""
        SELECT c.nome_candidato, c.partido, COUNT(v.voto) AS total_votos
        FROM candidatos c
        LEFT JOIN votos v ON c.numero_votacao = v.voto
        GROUP BY c.id_candidato, c.nome_candidato, c.partido
        ORDER BY c.nome_candidato ASC
    """)
    resultados = cursor.fetchall()
    print(f"\n{'Nome':<30} {'Partido':<25} {'Votos':>6}")
    print("-" * 65)
    for (nome, partido, total) in resultados:
        print(f"{nome:<30} {partido:<25} {total:>6}")

    # Votos nulos/brancos
    cursor.execute("SELECT COUNT(*) FROM votos WHERE voto = 0")
    nulos = cursor.fetchone()[0]
    print("-" * 65)
    print(f"{'Branco/Nulo':<30} {'':<25} {nulos:>6}")

    # Declaração do vencedor (RF002.03.03)
    cursor.execute("""
        SELECT c.nome_candidato, c.numero_votacao, c.partido, COUNT(v.voto) AS total_votos
        FROM candidatos c
        LEFT JOIN votos v ON c.numero_votacao = v.voto
        GROUP BY c.id_candidato, c.nome_candidato, c.numero_votacao, c.partido
        ORDER BY total_votos DESC
    """)
    todos = cursor.fetchall()
    print()
    if not todos or todos[0][3] == 0:
        print("=" * 65)
        print(f"{'Nenhum voto registrado ainda.':^65}")
        print("=" * 65)
    else:
        maior_votos = todos[0][3]
        empatados = [c for c in todos if c[3] == maior_votos]
        if len(empatados) == 1:
            vencedor = empatados[0]
            print("=" * 65)
            print(f"{'🏆  VENCEDOR DA ELEIÇÃO':^65}")
            print("=" * 65)
            print(f"  Nome    : \033[1m\033[37m{vencedor[0]}\033[0m")
            print(f"  Número  : \033[1m\033[37m{vencedor[1]}\033[0m")
            print(f"  Partido : \033[1m\033[37m{vencedor[2]}\033[0m")
            print(f"  Votos   : \033[1m\033[32m{vencedor[3]}\033[0m")
            print("=" * 65)
        else:
            print("=" * 65)
            print(f"{'⚠️   EMPATE NA ELEIÇÃO':^65}")
            print("=" * 65)
            print(f"  Não há vencedor. Os seguintes candidatos empataram")
            print(f"  com \033[1m\033[33m{maior_votos} voto(s)\033[0m cada:")
            print(f"  {'─' * 55}")
            for candidato in empatados:
                print(f"  {candidato[0]:<28} Nº {candidato[1]:<6} {candidato[2]}")
            print("=" * 65)

def estatistica_comparecimento():
    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]
    ausentes = total_eleitores - total_votos
    percentual = (total_votos / total_eleitores * 100) if total_eleitores > 0 else 0

    print(f"\nTotal de eleitores cadastrados : \033[1m\033[37m{total_eleitores}\033[0m")
    print(f"Total de votos computados      : \033[1m\033[37m{total_votos}\033[0m")
    print(f"Ausentes                       : \033[1m\033[37m{ausentes}\033[0m")
    print(f"Percentual de comparecimento   : \033[1m\033[37m{percentual:.2f}%\033[0m")

def votos_por_partido():
    cursor.execute("""
        SELECT c.partido, COUNT(v.voto) AS total_votos
        FROM candidatos c
        LEFT JOIN votos v ON c.numero_votacao = v.voto
        GROUP BY c.partido
        ORDER BY total_votos DESC
    """)
    resultados = cursor.fetchall()
    print(f"\n{'Partido':<30} {'Votos':>6}")
    print("-" * 38)
    for (partido, total) in resultados:
        print(f"{partido:<30} {total:>6}")

def listar_protocolos():
    cursor.execute("""
        SELECT v.protocolo_votacao, v.data_votacao
        FROM votos v
        ORDER BY v.data_votacao
    """)
    resultados = cursor.fetchall()
    if not resultados:
        print("\n\033[33mNenhum voto registrado ainda.\033[0m")
        return
    print(f"\n{'Protocolo':<28} {'Data/Hora':<22}")
    print("-" * 75)
    for (protocolo, data) in resultados:
        print(f"{protocolo:<28} {str(data):<22}")

def validar_integridade():
    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE votou IS NOT NULL")
    eleitores_que_votaram = cursor.fetchone()[0]

    print(f"\n{'─' * 50}")
    print(f"{'RELATÓRIO DE VALIDAÇÃO DE INTEGRIDADE':^50}")
    print(f"{'─' * 50}")
    print(f"\n  Votos registrados na urna         : \033[1m\033[37m{total_votos}\033[0m")
    print(f"  Eleitores com status 'Já Votou'   : \033[1m\033[37m{eleitores_que_votaram}\033[0m")
    print(f"\n{'─' * 50}")

    if total_votos == eleitores_que_votaram:
        print(f"\nINTEGRIDADE CONFIRMADA")
        print(f"     Os totais coincidem. Nenhuma inconsistência detectada.")
    else:
        diferenca = abs(total_votos - eleitores_que_votaram)
        print(f"\n\033[31mINCONSISTÊNCIA DETECTADA\033[0m")
        print(f"     Diferença de {diferenca} registro(s) entre a urna")
        print(f"     e o cadastro de eleitores que votaram.")

    print(f"\n{'─' * 50}")

# Fechar conexão
def fechar_conexao():
    cursor.close()
    conexao.close()

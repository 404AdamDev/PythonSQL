#   ============================================================
#   Sistema de Tarefas - Implementação com Classes em Python
#   Autor: 404AdamDev (Adam Vitor)
#   ============================================================

#   ============================
#   Inicialização do sistema
#   ============================

# Importação das bibliotecas necessárias e variaveis necessárias
from sqlalchemy import create_engine, text
from datetime import datetime
import time
import hashlib
import os
from enum import Enum

engine = None


#   ================================
#   Definição do modelo de dados
#   ================================

# Função para criar as tabelas no banco de dados
def estruturar_banco(connetion, dbNome):
    sql_users = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        nome VARCHAR(120) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE KEY,
        senha_hash VARCHAR(255) NOT NULL,
        criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """

    sql_tasks = """
    CREATE TABLE IF NOT EXISTS tarefas (
        id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	    usuario_id INT UNSIGNED NOT NULL,
        titulo VARCHAR(200) NOT NULL,
        descricao TEXT NULL,
        status ENUM('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA') NOT NULL DEFAULT 'PENDENTE',
        criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        concluido_em DATETIME NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """

    connetion.execute(text(f"CREATE DATABASE IF NOT EXISTS `{dbNome}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    connetion.execute(text(f"USE `{dbNome}`"))
    connetion.execute(text(sql_users))
    connetion.execute(text(sql_tasks))
    connetion.commit()


#   ======================
#   Funções do sistema
#   ======================

# Função para gerar hash de uma string
def gerar_hash(string):
    hash = hashlib.sha256()
    hash.update(string.encode('utf-8'))
    return hash.hexdigest()

# Função para inserir um novo usuário
def inserir_user(connetion):
    print("=== Inserindo novo usuário ===\nPor favor, preencha as informações abaixo:\n")
    
    userName = input("Digite o nome do usuário (ex: Blue Zão):\n>> ")
    userEmail = input("Digite o email do usuário (ex: bluezzao@gmail.com):\n>> ")
    userSenha = input("Digite a senha do usuário (ex: blue123):\n>> ")
    
    dbQuery = text("SELECT id FROM usuarios WHERE nome = :nome OR email = :email")
    dbResult = connetion.execute(dbQuery, {"nome": userName, "email": userEmail}).fetchall()
    
    if dbResult:
        print("\nNome ou email já cadastrado no sistema!")
        return
    
    dbQuery = text("INSERT INTO usuarios (nome, email, senha_hash) VALUES (:nome, :email, :senha)")
    connetion.execute(dbQuery, {"nome": userName, "email": userEmail, "senha": gerar_hash(userSenha)})
    connetion.commit()
    
    dbId = connetion.execute(text("SELECT LAST_INSERT_ID()")).scalar()
    print(f"\nUsuário '{userName}' cadastrado com sucesso! ID: {dbId}")

# Função para listar todos os usuários
def listar_users(connetion):
    print("=== Listando usuários ===")

    dbQuery = text("SELECT * FROM usuarios")
    dbRows = connetion.execute(dbQuery).fetchall()
    
    if not dbRows:
        print("\nNenhum usuário cadastrado!")
        return
    
    for row in dbRows:
        print(f"ID: {row.id} | Nome: {row.nome} | Email: {row.email} | Senha (hash): {row.senha_hash} | Criado em: {row.criado_em}")

# Função para inserir uma nova tarefa
def inserir_task(connetion):
    print("=== Inserindo nova tarefa ===\nPor favor, preencha as informações abaixo:\n")
    
    tarefaUser = input("Digite o nome (ou ID) do usuário para o qual a tarefa será cadastrada (ex. João Cleber / ex. 1):\n>> ")
    tarefaTitle = input("Digite o título da tarefa (ex. Fazer Compras):\n>> ")
    tarefaDesc = input("Digite a descrição da tarefa (ex. Fazer a compra do mês esse final de semana):\n>> ")
    tarefaStatus = input("Digite o status da tarefa (ex. PENDENTE):\n>> ").upper()
    
    dbUser = None
    if tarefaUser.isdigit():
        dbQuery = text("SELECT id FROM usuarios WHERE id = :id")
        dbUser = connetion.execute(dbQuery, {"id": int(tarefaUser)}).fetchone()
    else:
        dbQuery = text("SELECT id FROM usuarios WHERE LOWER(nome) = LOWER(:nome)")
        dbUser = connetion.execute(dbQuery, {"nome": tarefaUser}).fetchone()
        
    if not dbUser:
        print("\nUsuário não encontrado!")
        return
    
    if tarefaStatus not in ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"):
        print("\nStatus inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
        return
    
    dbQuery = text("INSERT INTO tarefas (usuario_id, titulo, descricao, status) VALUES (:id, :titulo, :descricao, :status)")
    connetion.execute(dbQuery, {"id": dbUser.id, "titulo": tarefaTitle, "descricao": tarefaDesc, "status": tarefaStatus})
    connetion.commit()
    
    print(f"\nTarefa '{tarefaTitle}' cadastrada com sucesso! Usuário responsável: {dbUser.id}")
            
# Função para listar as tarefas por filtros
def listar_tasks(connetion):
    print("=== Listar tarefas ===")
    check = text("SELECT COUNT(*) FROM tarefas")
    total = connetion.execute(check).scalar()

    if total == 0:
        print("\nNenhuma tarefa cadastrada!")
        return 

    print("Escolha o tipo de filtragem que quer realizar:\n1. Mostrar tudo\n2. Filtrar usuário\n3. Filtrar status")
    opcao = input("Sua escolha:\n>> ")

    os.system("cls")
    print("=== Listar tarefas ===")
    
    if opcao == "1":
        dbQuery = text("SELECT * FROM tarefas")
        dbRows = connetion.execute(dbQuery).fetchall() 
    elif opcao == "2":
        userNameOrId = input("Digite o nome (ou id) do usuário:\n>> ")
        
        dbUser = None
        if userNameOrId.isdigit():
            dbQuery = text("SELECT id FROM usuarios WHERE id = :id")
            dbUser = connetion.execute(dbQuery, {"id": int(userNameOrId)}).fetchone()
        else:
            dbQuery = text("SELECT id FROM usuarios WHERE LOWER(nome) = LOWER(:nome)")
            dbUser = connetion.execute(dbQuery, {"nome": userNameOrId}).fetchone()
            
        if not dbUser:
            print("Usuário não encontrado!")
            return

        os.system("cls")
        print("=== Listar tarefas ===")
        
        dbQuery = text("SELECT * FROM tarefas WHERE usuario_id = :id")
        dbRows = connetion.execute(dbQuery, {"id": dbUser.id}).fetchall()
    elif opcao == "3":
        taskStatus = input("Digite o status da(s) tarefa(s):\n>> ").upper()
        if taskStatus not in ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"):
            print("Status inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
            return
        
        os.system("cls")
        print("=== Listar tarefas ===")
        
        dbQuery = text("SELECT * FROM tarefas WHERE status = :status")
        dbRows = connetion.execute(dbQuery, {"status": taskStatus}).fetchall()
    else:
        print("Opção inválida!")
        return
    
    if not dbRows:
        print("Nenhuma tarefa encontrada!")
        return
    
    for row in dbRows:
        print(f"ID: {row.id} | ID Usuário resposnável: {row.usuario_id} | Titulo: {row.titulo} | Descrição: {row.descricao} | Status: {row.status} | Concluido em: {row.concluido_em if row.concluido_em is not None else 'Não Concluída'} | Criado em: {row.criado_em}")

# Função para atualizar uma tarefa existente
def atualizar_task(connetion):
    print("=== Atualizar tarefa ===\nPor favor, preencha as informações abaixo:\n")
    check = text("SELECT COUNT(*) FROM tarefas")
    total = connetion.execute(check).scalar()

    if total == 0:
        print("\nNenhuma tarefa cadastrada!")
        return 

    taskId = input("Digite o ID da tarefa que deseja atualizar:\n>> ")
    dbQuery = text("SELECT * FROM tarefas WHERE id = :id")
    dbRow = connetion.execute(dbQuery, {"id": taskId}).fetchone()

    if dbRow:
        print(f"\nTarefa encontrada: ID: {dbRow.id} | ID Usuário resposnável: {dbRow.usuario_id} | Titulo: {dbRow.titulo} | Descrição: {dbRow.descricao} | Status: {dbRow.status} | Concluido em: {dbRow.concluido_em if dbRow.concluido_em is not None else 'Não Concluída'} | Criado em: {dbRow.criado_em}\n")
    else:
        print("Tarefa não encontrada!")
        return
        
    os.system("cls")
    print("Escolha o campo que deseja atualizar:\n1. Usuário responsável\n2. Título\n3. Descrição\n4. Status")
    opcao = input("Sua escolha:\n>> ")

    os.system("cls")
    if opcao == "1":
        novo_valor = input("Digite o novo ID do usuário responsável:\n>> ")
        dbQuery = text("UPDATE tarefas SET usuario_id = :valor WHERE id = :id")
        connetion.execute(dbQuery, {"valor": novo_valor, "id": taskId})
    elif opcao == "2":
        novo_valor = input("Digite o novo título da tarefa:\n>> ")
        dbQuery = text("UPDATE tarefas SET titulo = :valor WHERE id = :id")
        connetion.execute(dbQuery, {"valor": novo_valor, "id": taskId})
    elif opcao == "3":
        novo_valor = input("Digite a nova descrição da tarefa:\n>> ")
        dbQuery = text("UPDATE tarefas SET descricao = :valor WHERE id = :id")
        connetion.execute(dbQuery, {"valor": novo_valor, "id": taskId})
    elif opcao == "4":
        novo_valor = input("Digite o novo status da tarefa (ex. PENDENTE):\n>> ").upper()
        if novo_valor not in ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"):
            print("Status inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
            return

        dbQuery = text("UPDATE tarefas SET status = :valor, concluido_em = NULL WHERE id = :id")
        connetion.execute(dbQuery, {"valor":novo_valor, "id": taskId})

        if novo_valor == "CONCLUIDA":
            dbQuery = text("UPDATE tarefas SET concluido_em = NOW() WHERE id = :id")
            connetion.execute(dbQuery, {"id": taskId})
    else:
        print("Opção inválida!")
        return

    connetion.commit()
    print(f"\nTarefa ID '{taskId}' atualizada com sucesso!")

# Função para remover uma tarefa existente
def remover_task(connetion):
    print("=== Remover tarefa ===")
    check = text("SELECT COUNT(*) FROM tarefas")
    total = connetion.execute(check).scalar()

    if total == 0:
        print("\nNenhuma tarefa cadastrada!")
        return 
    
    taskId = input("Digite o ID da tarefa que deseja remover:\n>> ")

    dbQuery = text("DELETE FROM tarefas WHERE id = :id")
    dbResult = connetion.execute(dbQuery, {"id": taskId})
    
    if dbResult.rowcount == 0:
        print("\nTarefa não encontrada!")
        return
    
    connetion.commit()
    print(f"Tarefa ID {taskId} removida com sucesso!")

# Função para inicializar o sistema
def inicializar_sistema():
    global engine

    os.system("cls")
    print("=== Sistema de tarefas ===\nBem vindo ao sistema de tarefas!\nAqui você poderá gerenciar usuários e tarefas de forma simples e eficiente.\nAntes de começar, precisamos configurar o acesso ao banco de dados MySQL.\n")

    print("Por favor, insira as informações de conexão com o MySQL abaixo.")
    dbUser = input("Usuário do MySQL (root): ") or "root"
    dbSenha = input("Senha do MySQL (vazio): ") or ""
    dbBanco = input("Nome do banco de dados (taskflow_db): ") or "taskflow_db"
    dbPort = int(input("Porta do MySQL (3306): ") or 3306)
    dbHost = input("Host do MySQL (localhost): ") or "localhost"

    dbUrl = f"mysql+pymysql://{dbUser}:{dbSenha}@{dbHost}:{dbPort}?charset=utf8mb4"
    print(f"\nConectando ao banco de dados em: {dbUrl}")
    time.sleep(1)
    incio = time.time()
    
    try:
        engine = create_engine(dbUrl, echo=False, future=True)
        
        with engine.connect() as dbConnetion:
            estruturar_banco(dbConnetion, dbBanco)
        
        newDbUrl = f"mysql+pymysql://{dbUser}:{dbSenha}@{dbHost}:{dbPort}/{dbBanco}?charset=utf8mb4"
        engine = create_engine(newDbUrl, echo=False, future=True)
        
        with engine.connect() as dbConnetion:
            result = dbConnetion.execute(text("SELECT 1"))
            result.scalar()
            
        fim = time.time()
        os.system("cls")
        print(f"Conectado ao banco de dados {dbBanco} com sucesso! Tempo demorado: {fim - incio:.2f} segundos.\n")
    except Exception as e:
        fim = time.time()
        
        os.system("cls")
        print(f"Erro ao conectar ao banco de dados: {e}. Tempo decorrido: {fim - incio:.2f} segundos.\n")
        
        again = input("Deseja tentar novamente? (s/n)\n>> ").upper()
        if again == "N":
            print("Encerrando o sistema...")
            exit(1)
        
        inicializar_sistema()
        return
    
    input("Pressione ENTER para continuar...")

    os.system("cls")
    print("Iniciando o sistema...")
    time.sleep(1)
    menu()

# Menu principal do sistema
def menu():
    with engine.connect() as dbConnetion:
        while True:
            os.system("cls")
            print("Sistema de tarefas - Menu")
            print("1. Inserir Usuário\n2. Listar Usuários\n3. Inserir Tarefa\n4. Listar Tarefas\n5. Atualizar Tarefa\n6. Remover Tarefa")
            opcao = input("Sua escolha:\n>> ")

            os.system("cls")
            if opcao == "1":
                inserir_user(dbConnetion)
            elif opcao == "2":
                listar_users(dbConnetion)
            elif opcao == "3":
                inserir_task(dbConnetion)
            elif opcao == "4":
                listar_tasks(dbConnetion)
            elif opcao == "5":
                atualizar_task(dbConnetion)
            elif opcao == "6":
                remover_task(dbConnetion)
            else:
                print("Opção inválida!\n")
                again = input("Deseja tentar novamente? (s/n)\n>> ").upper()
                if again == "N":
                    break

            input("\nPressione ENTER para continuar...")
    
# Iniciar o sistema
inicializar_sistema()
#   ============================================================
#   Sistema de Tarefas - Implementação com Classes em Python
#   Autor: 404AdamDev (Adam Vitor)
#   ============================================================

#   ============================
#   Inicialização do sistema
#   ============================

# Importação das bibliotecas necessárias e variaveis necessárias
from sqlalchemy import create_engine, text, Column, Text, Enum, DateTime, String, Table, ForeignKey, Integer, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.dialects.mysql import INTEGER
from datetime import datetime
import time
import hashlib
import os

engine = None
base = declarative_base()

#   ================================
#   Definição do modelo de dados
#   ================================

# Classe para representar usuários
class usuario(base):
    __tablename__ = "usuarios"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    tarefas = relationship('tarefa', back_populates="usuarios", cascade="all, delete-orphan", passive_deletes=True)

# Classe para representar tarefas
class tarefa(base):
    __tablename__ = "tarefas"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    usuario_id = Column(INTEGER(unsigned=True), ForeignKey('usuarios.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text)
    status = Column(Enum('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA', name='enum_status'), nullable=False, default='PENDENTE')
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
    concluido_em = Column(DateTime)

    usuarios = relationship('usuario', back_populates="tarefas")

#   ======================
#   Funções do sistema
#   ======================

# Função para gerar hash de uma string
def gerar_hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

# Função para inserir um novo usuário
def inserir_user(session):
    print("=== Inserindo novo usuário ===\nPor favor, preencha as informações abaixo:\n")
    
    userName = input("Digite o nome do usuário (ex: Blue Zão):\n>> ")
    userEmail = input("Digite o email do usuário (ex: bluezzao@gmail.com):\n>> ")
    userSenha = input("Digite a senha do usuário (ex: blue123):\n>> ")
    
    if session.query(usuario).filter(usuario.email == userEmail or func.lower(usuario.nome) == userName.lower).first():
        print("Nome ou email já cadastrado!")
        return
    
    newUser = usuario(
        nome=userName,
        email=userEmail,
        senha_hash=gerar_hash(userSenha)
    )

    session.add(newUser)
    session.commit()
    print(f"Usuário '{userName}' cadastrado com sucesso! ID: {newUser.id}")

# Função para listar todos os usuários
def listar_users(session):
    print("=== Listando usuários ===")

    usersList = session.query(usuario).all()
    if not usersList:
        print("\nNenhum usuário cadastrado!")
        return
    
    for user in usersList:
        print(f"ID: {user.id} | Nome: {user.nome} | Email: {user.email} | Senha (hash): {user.senha_hash} | Criado em: {user.criado_em}")

# Função para inserir uma nova tarefa
def inserir_task(session):
    print("=== Inserindo nova tarefa ===\nPor favor, preencha as informações abaixo:\n")
    
    tarefaUser = input("Digite o nome (ou ID) do usuário para o qual a tarefa será cadastrada (ex. João Cleber / ex. 1):\n>> ")
    tarefaTitle = input("Digite o título da tarefa (ex. Fazer Compras):\n>> ")
    tarefaDesc = input("Digite a descrição da tarefa (ex. Fazer a compra do mês esse final de semana):\n>> ")
    tarefaStatus = input("Digite o status da tarefa (ex. PENDENTE):\n>> ").upper()
    
    dbUser = None
    if tarefaUser.isdigit():
        dbUser = session.query(usuario).filter(usuario.id == int(tarefaUser)).first()
    else:
        dbUser = session.query(usuario).filter(func.lower(usuario.nome) == tarefaUser.lower()).first()
        
    if not dbUser:
        print("\nUsuário não encontrado!")
        return
    
    if tarefaStatus not in ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"):
        print("\nStatus inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
        return
    
    newTask = tarefa(
        usuario_id=dbUser.id,
        titulo=tarefaTitle,
        descricao=tarefaDesc,
        status=tarefaStatus
    )

    session.add(newTask)
    session.commit()
    print(f"\nTarefa '{tarefaTitle}' cadastrada com sucesso! Usuário responsável: {dbUser.id}")
            
# Função para listar as tarefas por filtros
def listar_tasks(session):
    print("=== Listar tarefas ===")

    total = session.query(tarefa).count()
    if total == 0:
        print("Nenhuma tarefa cadastrada!")
        return

    print("Escolha o tipo de filtragem que quer realizar:\n1. Mostrar tudo\n2. Filtrar usuário\n3. Filtrar status")
    opcao = input("Sua escolha:\n>> ")

    os.system("cls")
    print("=== Listar tarefas ===")
    
    if opcao == "1":
        taskList = session.query(tarefa).all()
    elif opcao == "2":
        userNameOrId = input("Digite o nome (ou id) do usuário:\n>> ")
        
        dbUser = None
        if userNameOrId.isdigit():
            dbUser = session.query(usuario).filter(usuario.id == int(userNameOrId)).first()
        else:
            dbUser = session.query(usuario).filter(func.lower(usuario.nome) == userNameOrId.lower()).first()
            
        if not dbUser:
            print("Usuário não encontrado!")
            return
        
        taskList = session.query(tarefa).filter(tarefa.usuario_id == dbUser.id).all()
    elif opcao == "3":
        taskStatus = input("Digite o status da(s) tarefa(s):\n>> ").upper()
        if taskStatus not in ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"):
            print("Status inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
            return
        
        taskList = session.query(tarefa).filter(tarefa.status == taskStatus).all()
    else:
        print("Opção inválida!")
        return
    
    os.system("cls")
    print("=== Listar tarefas ===")
    
    if not taskList:
        print("Nenhuma tarefa encontrada!")
        return
    
    for task in taskList:
        print(f"ID: {task.id} | ID Usuário resposnável: {task.usuario_id} | Titulo: {task.titulo} | Descrição: {task.descricao} | Status: {task.status} | Concluido em: {task.concluido_em if task.concluido_em is not None else 'Não Concluída'} | Criado em: {task.criado_em}")

# Função para atualizar uma tarefa existente
def atualizar_task(session):
    print("=== Atualizar tarefa ===")

    total = session.query(tarefa).count()
    if total == 0:
        print("Nenhuma tarefa cadastrada!")
        return

    os.system("cls")
    print("=== Atualizar tarefa ===\nPor favor, preencha as informações abaixo:\n")
    taskId = input("Digite o ID da tarefa que deseja atualizar:\n>> ")
    task = session.query(tarefa).filter(tarefa.id == taskId).first()

    if not task:
        print("Tarefa não encontrada!")
        return
        
    os.system("cls")
    print(f"Tarefa encontrada:\nID: {task.id} | ID Usuário resposnável: {task.usuario_id} | Titulo: {task.titulo} | Descrição: {task.descricao} | Status: {task.status} | Concluido em: {task.concluido_em if task.concluido_em is not None else 'Não Concluída'} | Criado em: {task.criado_em}\n")
    print("Escolha o campo que deseja atualizar:\n1. Usuário responsável\n2. Título\n3. Descrição\n4. Status")
    opcao = input("Sua escolha:\n>> ")

    os.system("cls")
    if opcao == "1":
        novo_valor = input("Digite o novo ID do usuário responsável:\n>> ")
        if not int(novo_valor):
            print("ID inválido!")
            return
        
        task.usuario_id = int(novo_valor)
    elif opcao == "2":
        novo_valor = input("Digite o novo título da tarefa:\n>> ")
        task.titulo = novo_valor
    elif opcao == "3":
        novo_valor = input("Digite a nova descrição da tarefa:\n>> ")
        task.descricao = novo_valor
    elif opcao == "4":
        novo_valor = input("Digite o novo status da tarefa (ex. PENDENTE):\n>> ").upper()
        if novo_valor not in ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"):
            print("Status inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
            return

        task.status = novo_valor
        if novo_valor == "CONCLUIDA":
            task.concluido_em = datetime.now()
    else:
        print("Opção inválida!")
        return

    session.commit()
    print(f"\nTarefa ID '{taskId}' atualizada com sucesso!")

# Função para remover uma tarefa existente
def remover_task(session):
    print("=== Remover tarefa ===")
    
    total = session.query(tarefa).count()
    if total == 0:
        print("Nenhuma tarefa cadastrada!")
        return
    
    taskId = input("Digite o ID da tarefa que deseja remover:\n>> ")
    task = session.query(tarefa).filter(tarefa.id == taskId).first()
    
    if not task:
        print("Tarefa não encontrada!")
        return
    
    session.delete(task)
    session.commit()
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
    print(f"\nConectando ao banco de dados em: '{dbUrl}'...")
    time.sleep(1)
    incio = time.time()
    
    try:
        engine = create_engine(dbUrl, echo=False, future=True)
        
        with engine.connect() as dbConnetion:
            dbConnetion.execute(text(f"CREATE DATABASE IF NOT EXISTS `{dbBanco}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            dbConnetion.execute(text(f"USE `{dbBanco}`"))
        
        newDbUrl = f"mysql+pymysql://{dbUser}:{dbSenha}@{dbHost}:{dbPort}/{dbBanco}?charset=utf8mb4"
        engine = create_engine(newDbUrl, echo=False, future=True)
        
        with engine.connect() as dbConnetion:
            result = dbConnetion.execute(text("SELECT 1"))
            result.scalar()
            
        fim = time.time()
        os.system("cls")
        print(f"Conectado ao banco de dados {dbBanco} com sucesso! Tempo decorrido: {fim - incio:.2f} segundos.\n")
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
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    newSession = session()

    while True:
        os.system("cls")
        print("Sistema de tarefas - Menu")
        print("1. Inserir Usuário\n2. Listar Usuários\n3. Inserir Tarefa\n4. Listar Tarefas\n5. Atualizar Tarefa\n6. Remover Tarefa")
        opcao = input("Sua escolha:\n>> ")

        os.system("cls")
        if opcao == "1":
            inserir_user(newSession)
        elif opcao == "2":
            listar_users(newSession)
        elif opcao == "3":
            inserir_task(newSession)
        elif opcao == "4":
            listar_tasks(newSession)
        elif opcao == "5":
            atualizar_task(newSession)
        elif opcao == "6":
            remover_task(newSession)
        else:
            print("Opção inválida!\n")
            again = input("Deseja tentar novamente? (s/n)\n>> ").upper()
            if again == "N":
                break

        input("\nPressione ENTER para continuar...")
    
# Iniciar o sistema
inicializar_sistema()
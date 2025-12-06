#   ============================================================
#   Sistema de Tarefas - Implementação com Classes em Python
#   Autor: 404AdamDev (Adam Vitor)
#   ============================================================

#   ============================
#   Inicialização do sistema
#   ============================

# Importação das bibliotecas necessárias
from datetime import datetime
import time
import hashlib
import os
from enum import Enum

# Listas para armazenar usuários e tarefas
users = []
tasks = []


#   =========================
#   Definição das classes
#   =========================

# Função para gerar hash de uma string
def gerar_hash(string):
    hash = hashlib.sha256()
    hash.update(string.encode('utf-8'))
    return hash.hexdigest()

# Classe para representar usuários
class usuarios:
    _user_id = 1

    def __init__(self, nome, email, senha):
        self.id = usuarios._user_id
        usuarios._user_id += 1

        self.nome = nome
        self.email = email
        self.senha_hash = gerar_hash(senha)
        
        self.criado_em = datetime.now()
        users.append(self)

# Enum para representar os status das tarefas
class status_enum(Enum):
    PENDENTE = 1, 
    EM_ANDAMENTO = 2, 
    CONCLUIDA = 3, 
    CANCELADA = 4

# Classe para representar tarefas
class tarefas:
    _task_id = 1

    def __init__(self, usuario_id, titulo, descricao, status=status_enum.PENDENTE, concluido_em=None):
        self.id = tarefas._task_id
        tarefas._task_id += 1
        self.usuario_id = usuario_id

        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        if status == status_enum.CONCLUIDA:
            concluido_em = datetime.now()

        self.criado_em = datetime.now()
        self.concluido_em = concluido_em
        tasks.append(self)

    def alterar_item(self, item, novo_valor):
        itens = ["usuario_id", "titulo", "descricao", "status", "concluido_em"]

        if item in itens:
            setattr(self, item, novo_valor)

            if item == "status":
                if novo_valor == status_enum.CONCLUIDA:
                    self.concluido_em = datetime.now()
                else:
                    self.concluido_em = None   
        else:
            print(f"O campo '{item}' não é válido para alteração.")


#  ======================
#  Funções do sistema
#  ======================

# Função para inserir um novo usuário
def inserir_user():
    print("=== Inserindo novo usuário ===\nPor favor, preencha as informações abaixo:\n")
    userName = input("Digite o nome do usuário (ex: Blue Zão):\n>> ")
    userEmail = input("Digite o email do usuário (ex: bluezzao@gmail.com):\n>> ")
    userSenha = input("Digite a senha do usuário (ex: blue123):\n>> ")

    for user in users:
        if user.nome == userName or user.email == userEmail:
            print("\nNome ou email já cadastrado no sistema!")
            return

    novo_user = usuarios(userName, userEmail, userSenha)
    print(f"\nUsuário '{novo_user.nome}' cadastrado com sucesso! ID: {novo_user.id}")

# Função para listar todos os usuários
def listar_users():
    print("=== Listando usuários ===")

    if len(users) <= 0 :
        print("\nNenhum usuário cadastrado!")
    
    for user in users:
        print(f"ID: {user.id} | Nome: {user.nome} | Email: {user.email} | Senha (hash): {user.senha_hash} | Criado em: {user.criado_em}")

# Função para inserir uma nova tarefa
def inserir_task():
    print("=== Inserindo nova tarefa ===\nPor favor, preencha as informações abaixo:\n")
    tarefaUser = input("Digite o nome (ou ID) do usuário para o qual a tarefa será cadastrada (ex. João Cleber / ex. 1):\n>> ")
    tarefaTitle = input("Digite o título da tarefa (ex. Fazer Compras):\n>> ")
    tarefaDesc = input("Digite a descrição da tarefa (ex. Fazer a compra do mês esse final de semana):\n>> ")
    tarefaStatus = input("Digite o status da tarefa (ex. PENDENTE):\n>> ")
    
    usuario_id = 0
    for user in users:
        if tarefaUser.isdigit():
            if user.id == int(tarefaUser):
                usuario_id = int(tarefaUser)
                break
        else:
            if user.nome.lower() == tarefaUser.lower():
                usuario_id = user.id
                break
    else:
        print("\nUsuário não encontrado!")
        return
    
    tarefaStatus = tarefaStatus.upper()
    if tarefaStatus not in status_enum.__members__:
        print("\nStatus inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
        return
    status = status_enum[tarefaStatus]
    
    nova_task = tarefas(usuario_id, tarefaTitle, tarefaDesc, status)
    print(f"\nTask '{nova_task.titulo}' criada com sucesso! Usuário responsável: {nova_task.usuario_id}")
            
# Função para listar as tarefas por filtros
def listar_tasks():
    print("=== Listando Tarefas ===")
    if len(tasks) <= 0 :
        print("\nNenhuma tarefa cadastrada!")
        return

    print("Escolha o tipo de filtragem que quer realizar:\n1. Mostrar tudo\n2. Filtrar usuário\n3. Filtrar status")
    opcao = input("Sua escolha:\n>> ")

    os.system("cls")
    print("=== Listando Tarefas ===\n")
    if opcao == "1":
        for task in tasks:
            print(f"ID: {task.id} | ID Usuário resposnável: {task.usuario_id} | Titulo: {task.titulo} | Descrção: {task.descricao} | Status: {task.status} | Concluido em: {task.concluido_em if task.concluido_em is not None else 'Não Concluída'} | Criado em: {task.criado_em}")
    elif opcao == "2":
        userNameOrId = input("\nDigite o nome (ou id) do usuário:\n>> ")
        
        usuario_id = 0
        for user in users:
            if userNameOrId.isdigit():
                if user.id == int(userNameOrId):
                    usuario_id = int(userNameOrId)
                    break
            else:
                if user.nome.lower() == userNameOrId.lower():
                    usuario_id = user.id
                    break

        os.system("cls")
        print("=== Listando Tasks ===")
        for task in tasks:
            if task.usuario_id == usuario_id:
                print(f"ID: {task.id} | ID Usuário resposnável: {task.usuario_id} | Titulo: {task.titulo} | Descrção: {task.descricao} | Status: {task.status} | Concluido em: {task.concluido_em if task.concluido_em is not None else 'Não Concluída'} | Criado em: {task.criado_em}")
    elif opcao == "3":
        taskStatus = input("\nDigite o status da(s) tarefa(s):\n>> ").upper()

        if taskStatus not in status_enum.__members__:
            print("\nStatus inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
            return
        status = status_enum[taskStatus]

        os.system("cls")
        print("=== Listando Tasks ===")
        for task in tasks:
            if task.status == status:
                print(f"ID: {task.id} | ID Usuário resposnável: {task.usuario_id} | Titulo: {task.titulo} | Descrção: {task.descricao} | Status: {task.status} | Concluido em: {task.concluido_em if task.concluido_em is not None else 'Não Concluída'} | Criado em: {task.criado_em}")
    else:
        print("Opção inválida!")
        return

# Função para atualizar uma tarefa existente
def atualizar_task():
    print("=== Atualizar tarefa ===")
    if len(tasks) <= 0 :
        print("\nNenhuma tarefa cadastrada!")
        return

    taskUpdate = input("Digite o ID da tarefa que deseja atualizar:\n>> ")
    for task in tasks:
        if task.id == int(taskUpdate):
            print(f"\nTarefa encontrada: ID: {task.id} | ID Usuário resposnável: {task.usuario_id} | Titulo: {task.titulo} | Descrção: {task.descricao} | Status: {task.status} | Concluido em: {task.concluido_em if task.concluido_em is not None else 'Não Concluída'} | Criado em: {task.criado_em}\n")
            taskUpdate = task
            break
    else:
        print("\nTarefa não encontrada!")
        return
    
    os.system("cls")
    print("Escolha o campo que deseja atualizar:\n1. Usuário responsável\n2. Título\n3. Descrição\n4. Status")
    opcao = input("Sua escolha:\n>> ")

    os.system("cls")
    if opcao == "1":
        novo_valor = input("Digite o novo ID do usuário responsável:\n>> ")
        task.alterar_item("usuario_id", int(novo_valor))
    elif opcao == "2":
        novo_valor = input("Digite o novo título da tarefa:\n>> ")
        task.alterar_item("titulo", novo_valor)
    elif opcao == "3":
        novo_valor = input("Digite a nova descrição da tarefa:\n>> ")
        task.alterar_item("descricao", novo_valor)
    elif opcao == "4":
        novo_valor = input("Digite o novo status da tarefa (ex. PENDENTE):\n>> ").upper()
        if novo_valor not in status_enum.__members__:
            print("\nStatus inválido! Use: PENDENTE, EM_ANDAMENTO, CONCLUIDA ou CANCELADA.")
            return
        
        status = status_enum[novo_valor]
        task.alterar_item("status", status)
    else:
        print("Opção inválida!")
        return

    print(f"\nTask ID '{taskUpdate.id}' atualizada com sucesso!")

# Função para remover uma tarefa existente
def remover_task():
    print("=== Remover tarefa ===")
    if len(tasks) <= 0 :
        print("\nNenhuma tarefa cadastrada!")
        return

    taskRemove = input("Digite o ID da tarefa que deseja remover:\n>> ")
    
    os.system("cls")
    for task in tasks:
        if task.id == int(taskRemove):
            tasks.remove(task)
            print(f"\nTarefa ID '{task.id}' removida com sucesso!")
            break
    else:
        print("\nTarefa não encontrada!")
        return

#  Inicialização do sistema
def inicializar_sistema():
    os.system("cls")
    print("=== Sistema de tarefas ===\nBem vindo ao sistema de tarefas!\nAqui você poderá gerenciar usuários e tarefas de forma simples e eficiente.\n")
    input("\nPressione ENTER para continuar...")
    
    os.system("cls")
    print("Iniciando o sistema...")
    time.sleep(1)
    menu()

# Menu principal do sistema
def menu():
    while True:
        os.system("cls")
        print("Sistema de tarefas - Menu")
        print("1. Inserir Usuário\n2. Listar Usuários\n3. Inserir Tarefa\n4. Listar Tarefas\n5. Atualizar Tarefa\n6. Remover Tarefa")
        opcao = input("Sua escolha:\n>> ")

        os.system("cls")
        if opcao == "1":
            inserir_user()
        elif opcao == "2":
            listar_users()
        elif opcao == "3":
            inserir_task()
        elif opcao == "4":
            listar_tasks()
        elif opcao == "5":
            atualizar_task()
        elif opcao == "6":
            remover_task()
        else:
            print("Opção inválida!\n")
            again = input("Deseja tentar novamente? (s/n)\n>> ").upper()
            if again == "N":
                break

        input("\nPressione ENTER para continuar...")

# Iniciar o sistema
inicializar_sistema()
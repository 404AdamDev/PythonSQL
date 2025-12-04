import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import hashlib

def conectar_sql():
    try:
        conexao = mysql.connector.connect (
            host="localhost",
            user="root",
            password="",
            database="taskflow_db",
            port="5506"
        )
        return conexao
    except Error as e:
        print("Erro ao conectar ao banco", e)
        return None
    
def inserir_user(conexao):
    print("Inserindo novo usuário...\nPor favor, preencha as informações abaixo:")
    userName = input("Digite o nome do usuário (ex: Blue Zão):\n")
    userEmail = input("Digite o email do usuário (ex: bluezzao@gmail.com):\n")
    userSenha = input("Digite a senha do usuário (ex: blue123):\n")

def listar_users(conexao):
    print("print")
    
def inserir_task(conexao):
    print("print")

def listar_tasks(conexao):
    print("print")

def atualizar_task(conexao):
    print("print")

def remover_task(conexao):
    print("print")

def menu():
    print("Conectando ao banco de dados...")
    conexao = conectar_sql()

    if conexao is None:
        input("\nPressione ENTER para continuar...")
        return
    else:
        print("Conectado ao banco de dados com sucesso!")
        input("\nPressione ENTER para continuar...")

    while True:
        os.system("cls")
        print("Sistema de tarefas - Menu")
        print("1. Inserir Usuário")
        print("2. Listar Usuários")
        print("3. Inserir Tarefa")
        print("4. Listar Tarefas")
        print("5. Atualizar Tarefa")
        print("6. Remover Tarefa")

        opcao = input("Sua escolha: ")

        os.system("cls")
        if opcao == "1":
            inserir_user(conexao)
        elif opcao == "2":
            listar_users(conexao)
        elif opcao == "3":
            inserir_task(conexao)
        elif opcao == "4":
            listar_tasks(conexao)
        elif opcao == "5":
            atualizar_task(conexao)
        elif opcao == "6":
            remover_task(conexao)
        else:
            print("Opção inválida!\n")
            again = input("Deseja tentar novamente? (s/n)\n").upper()
            if again == "N":
                break

        input("\nPressione ENTER para continuar...")
menu()
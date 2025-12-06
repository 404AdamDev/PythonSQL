# PythonSQL  
Sistema de gerenciamento de tarefas (TO-DO) com integração MySQL utilizando SQLAlchemy.

Este projeto contém duas versões do sistema:

- **main-class**: implementação sem uso de banco de dados, focada apenas em lógica e manipulação local.  
- **main-alchemy**: versão completa utilizando MySQL + SQLAlchemy para persistência e consultas estruturadas.

---

## 📁 Estrutura do Projeto

```
PythonSQL/
 ├── main-class/
 ├── main-alchemy/
 ├── README.md
 └── requirements.txt
```

---

## 🧰 Tecnologias Utilizadas

### Linguagem:
- Python 3.x

### Banco de Dados:
- MySQL

### ORM:
- SQLAlchemy 2.x

---

## 📦 Dependências Necessárias

Estas bibliotecas devem estar instaladas no ambiente virtual antes de rodar a aplicação:

```
greenlet==3.3.0
mysql-connector-python==9.5.0
PyMySQL==1.1.2
SQLAlchemy==2.0.44
typing_extensions==4.15.0
```

Para instalar automaticamente:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Funcionalidades

- Cadastro de usuários  
- Criação, edição e remoção de tarefas  
- Persistência de dados via MySQL  
- Contagem de tempo para conexão/estrutura do banco  
- Estruturação automática das tabelas na primeira execução  

---

## 🗄️ Configuração do Banco de Dados

O sistema solicita as credenciais logo no início:

- Usuário do MySQL  
- Senha  
- Nome do banco  
- Host  
- Porta  

O programa valida a conexão, cria o banco caso não exista e monta a estrutura de tabelas automaticamente.

---

## ▶️ Como Executar

### 1. Criar e ativar o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

### 3. Executar a versão desejada:

```bash
python main-class.py
# ou
python main-alchemy.py
```

---

## 📄 Licença

Este projeto é de uso livre para fins educacionais e pessoais.

---

## 📌 Autor

Desenvolvido por **404AdamDev**.

---

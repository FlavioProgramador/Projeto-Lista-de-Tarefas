# 📝 ACME - Protótipo de API Rest para Gestão de Tarefas

![Status](https://img.shields.io/badge/status-concluído-green)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)

Este projeto foi desenvolvido como parte do curso **Técnico em Desenvolvimento de Sistemas** da **Firjan Senai**. O objetivo foi criar um protótipo de API Rest para a empresa fictícia **ACME LTDA**, responsável por gerenciar tarefas com funcionalidades básicas de CRUD, consumida por uma interface moderna e reativa.

---

### 👨‍💻 Equipe do Projeto
- Flavio da Costa Marques
- Rafael Pereira

---

### 📚 Índice

- [Contexto do Projeto](#-contexto-do-projeto)
- [Principais Funcionalidades](#-principais-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Rodar o Projeto](#-como-rodar-o-projeto)

---

### 🎯 Contexto do Projeto

A empresa ACME LTDA solicitou o desenvolvimento de um protótipo de sistema para gestão de tarefas, com os seguintes requisitos:

- **Modelo de Tarefa:**
  - Título `(obrigatório)`
  - Descrição `(opcional)`
  - Data de início `(obrigatória)`
  - Data de término `(obrigatória)`
  - Status `(Pendente, Em Andamento ou Finalizada)`

- **Serviços da API:**
  - Inserir nova tarefa
  - Editar uma tarefa existente
  - Excluir uma tarefa
  - Procurar uma tarefa específica por **ID**
  - Listar todas as tarefas

---

### ✨ Principais Funcionalidades

- **Backend (API):**
  - Sistema CRUD completo para as tarefas.
  - Endpoints RESTful seguindo as melhores práticas de mercado.

- **Frontend (Interface):**
  - Visualização clara de todas as tarefas.
  - Formulário dinâmico para criação e edição de tarefas.
  - Exclusão e alteração de status com um clique.
  - Interface reativa e responsiva.

---

### 🚀 Tecnologias Utilizadas

- **Back-end:**
  - Python 3.11+
  - Django & Django Rest Framework
- **Banco de Dados:**
  - SQLite (padrão do Django)
- **Front-end:**
  - Vue.js 3 (Composition API)
  - Axios (para chamadas à API)

---

### ⚙️ Como Rodar o Projeto

**Pré-requisitos:** Ter `Git`, `Python 3.11+` e `Node.js` instalados na sua máquina.

**1️⃣ Clone o repositório:**
```bash
git clone https://github.com/FlavioProgramador/To_do_List.git
cd To_do_List


---

# Navegue até a pasta do backend (ajuste o nome se for diferente)
cd backend/

# Crie e ative o ambiente virtual
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale as dependências do Python
pip install -r requirements.txt

# Aplique as migrações do banco de dados
python manage.py migrate

# Crie um superusuário para acessar o Admin do Django
python manage.py createsuperuser

# Inicie o servidor do Django
python manage.py runserver

---

# Em um NOVO terminal, navegue até a pasta do frontend (ajuste se necessário)
cd frontend/

# Instale as dependências do Node.js
npm install

# Inicie o servidor de desenvolvimento do Vue
npm run dev

---

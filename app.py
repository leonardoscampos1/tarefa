import streamlit as st
import json
import os

# Função para carregar tarefas de um arquivo JSON
def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
    return {"A Planejar": [], "Em Progresso": [], "Concluídas": []}

# Função para salvar tarefas em um arquivo JSON
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# Carregando as tarefas
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()
tasks = st.session_state.tasks

# Título do aplicativo
st.title("Gerenciador de Tarefas")

# Input para adicionar uma nova tarefa
new_task = st.text_input("Adicionar nova tarefa")

# Verifica se a tarefa já existe em alguma das colunas
def is_task_duplicate(new_task, tasks):
    return new_task in tasks["A Planejar"] or new_task in tasks["Em Progresso"] or new_task in tasks["Concluídas"]

# Função para sanitizar o nome da tarefa (remover caracteres especiais e espaços)
def sanitize_task_name(task):
    return task.replace(' ', '_').replace("'", "_").replace('"', '_')

# Botão para adicionar tarefa
if st.button("Adicionar"):
    if new_task:
        if is_task_duplicate(new_task, tasks):
            st.warning(f"A tarefa '{new_task}' já existe!")  # Exibe um aviso se a tarefa for duplicada
        else:
            tasks["A Planejar"].append(new_task)
            save_tasks(tasks)  # Salva as tarefas após adicionar
            st.session_state.tasks = tasks  # Atualiza o estado das tarefas

# Criando as colunas
cols = st.columns(3)
columns = ["A Planejar", "Em Progresso", "Concluídas"]

# Exibindo as tarefas em cada coluna
for i, col_name in enumerate(columns):
    with cols[i]:
        st.header(col_name)
        for task_index, task in enumerate(tasks[col_name]):
            st.write(task)

            sanitized_task = sanitize_task_name(task)  # Sanitiza o nome da tarefa para a chave
            unique_key = f"{sanitized_task}_{col_name}_{task_index}"

            # Movendo as tarefas entre as colunas com ações rápidas
            if col_name == "A Planejar":
                if st.button(f"Iniciar '{task}'", key=f"start_{unique_key}"):
                    tasks[col_name].remove(task)
                    tasks["Em Progresso"].append(task)
                    save_tasks(tasks)  # Salva as tarefas após mover
                    st.session_state.tasks = tasks  # Atualiza o estado das tarefas
            elif col_name == "Em Progresso":
                if st.button(f"Concluir '{task}'", key=f"finish_{unique_key}"):
                    tasks[col_name].remove(task)
                    tasks["Concluídas"].append(task)
                    save_tasks(tasks)  # Salva as tarefas após mover
                    st.session_state.tasks = tasks  # Atualiza o estado das tarefas
            elif col_name == "Concluídas":
                if st.button(f"Reiniciar '{task}'", key=f"restart_{unique_key}"):
                    tasks[col_name].remove(task)
                    tasks["A Planejar"].append(task)
                    save_tasks(tasks)  # Salva as tarefas após mover
                    st.session_state.tasks = tasks  # Atualiza o estado das tarefas

# Salva as tarefas ao final, se necessário
save_tasks(tasks)

import json
import re
from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk

def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Erro: O arquivo {file_name} não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decodificar o arquivo {file_name}.")
        return []

def save_json(file_name, data):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Erro ao escrever no ficheiro. Verifique as permissões. \n{e}")

def validaData(data_str):
    try:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', data_str):
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")
        datetime.strptime(data_str, '%Y-%m-%d')
        return data_str
    except ValueError as e:
        raise ValueError(f"Erro ao validar a data: {e}")

def validaMatricula(matricula):
    pattern = re.compile(r'^[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}$')
    matricula = matricula.upper()
    if pattern.match(matricula):
        return matricula
    else:
        return None

def verificaIDInteiro(valor, default=None):
    while True:
        try:
            return int(input(valor) or default)
        except ValueError:
            print("Por favor, insira um número inteiro válido.")

def maiorIDLista(lista):
    if lista:
        return max(item['id'] for item in lista)
    return 1

def validaConfirmacao(valor):
    while True:
        resposta = input(valor).strip().upper()
        if resposta in ['S', 'N']:
            return resposta
        print("Resposta inválida. Por favor, insira 'S' para sim ou 'N' para não.")

def selecionaData(titulo, optional=False):
    selected_date = None
    
    def getData():
        nonlocal selected_date
        selected_date = cal.get_date()
        main.destroy()

    main = tk.Tk()
    main.title(titulo)
    anoCurrente = datetime.now().year
    cal = DateEntry(main, width=30, background='darkblue', foreground='white', borderwidth=2, year=anoCurrente)
    cal.pack(padx=50, pady=50)
    tk.Button(main, text="OK", command=getData).pack()
    main.mainloop()

    if selected_date:
        return selected_date.strftime('%Y-%m-%d')
    elif optional:
        return None
    else:
        raise ValueError("Data não selecionada.")

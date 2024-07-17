import json
import re
from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk
import beaupy

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

def selecionaData(titulo, default_date=None, optional=False):
    selected_date = None

    def getData():
        nonlocal selected_date
        selected_date = cal.get_date()
        main.destroy()

    main = tk.Tk()
    main.title(titulo)
    anoCurrente = datetime.now().year
    
    # Verifica se há uma data padrão fornecida e a converte para o formato DateEntry
    if default_date:
        default_date = datetime.strptime(default_date, '%Y-%m-%d').date()
    else:
        default_date = datetime.now().date()

    cal = DateEntry(main, width=30, background='darkblue', foreground='white', borderwidth=2, year=anoCurrente)
    cal.set_date(default_date)  # Define a data padrão no widget
    cal.pack(padx=50, pady=50)
    tk.Button(main, text="OK", command=getData).pack()
    main.mainloop()

    if selected_date:
        return selected_date.strftime('%Y-%m-%d')
    elif optional:
        return None
    else:
        raise ValueError("Data não selecionada.")
    
    import beaupy

def selecionaCliente(listCliente):
    clienteOpcao = [f"{cliente['id']} - {cliente['nome']}" for cliente in listCliente]
    clienteEscolha = beaupy.select(clienteOpcao, cursor='->', cursor_style='red', return_index=True)
    cliente_id = listCliente[clienteEscolha]['id']
    return cliente_id

def selecionaAutomovel(listAutomovel):
    opcoesAutomovel = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in listAutomovel]
    automovelecolha = beaupy.select(opcoesAutomovel, cursor='->', cursor_style='red', return_index=True)
    automovel_id = listAutomovel[automovelecolha]['id']
    return automovel_id


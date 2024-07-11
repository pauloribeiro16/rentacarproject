import json
import datetime
import re
import json
from datetime import datetime

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
        datetime.strptime(data_str, '%Y-%m-%d')  # Verifica se a data é válida
        return data_str
    except IOError as e:
         print(f"Erro ao validar a data \n{e}")

def validaMatricula(matricula):
    # Expressão regular para validar o formato AA-BB-22
    pattern = re.compile(r'^[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}$')
    # Converter para maiúsculas
    matricula = matricula.upper()
    # Verificar se o formato está correto
    if pattern.match(matricula):
        return matricula
    else:
        return None

def verificaIDInteiro(self, valor, default=None):
    while True:
        try:
            return int(input(valor) or default)
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
    
def maiorIDLista(lista):
    if lista:
        return max(item['id'] for item in lista)
    return 1
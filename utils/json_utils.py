import json

def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as error:
        print("Ocorreu um erro ao ler os dados:", error)

def save_json(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as error:
        print("Ocorreu um erro ao escrever os dados:", error)

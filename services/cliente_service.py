from utils.json_utils import load_json, save_json
from models.cliente import Cliente
import beaupy

class ClienteService:
    def __init__(self):
        self.listCliente = load_json('data/listcliente.json')

    def manage(self):
        while True:
            options = ["Listar Clientes", "Adicionar Cliente", "Atualizar Cliente", "Remover Cliente", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.list_items()
            elif choice == 1:
                self.add_item()
            elif choice == 2:
                self.update_item()
            elif choice == 3:
                self.remove_item()
            elif choice == 4:
                break

    def list_items(self):
        for item in self.listCliente:
            print(item)
 

    def add_item(self):
        id = int(input("ID: ")) # função para verificar id
        nome = input("Nome: ")
        nif = int(input("NIF: ")) # função para verificar nif
        dataNascimento = input("Data de Nascimento: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        novo_cliente = Cliente(id, nome, nif, dataNascimento, telefone, email)
        self.listCliente.append(novo_cliente.__dict__)
        self.save_changes()

    def update_item(self):
        id = int(input("ID do cliente a atualizar: "))
        for cliente in self.listCliente:
            if cliente['id'] == id:
                cliente['nome'] = input("Novo Nome: ") or cliente['nome']
                cliente['nif'] = int(input("Novo NIF: ") or cliente['nif']) # função para verificar id
                cliente['dataNascimento'] = input("Nova Data de Nascimento: ") or cliente['dataNascimento']
                cliente['telefone'] = input("Novo Telefone: ") or cliente['telefone']
                cliente['email'] = input("Novo Email: ") or cliente['email']
                self.save_changes()
                return
        print("Cliente não encontrado.")

    def remove_item(self):
        id = int(input("ID do cliente a remover: "))
        self.listCliente = [cliente for cliente in self.listCliente if cliente['id'] != id]
        self.save_changes()

    def save_changes(self):
        save_json('data/listcliente.json', self.listCliente)

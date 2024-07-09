from utils.json_utils import load_json, save_json
from models.cliente import Cliente
import beaupy

class ClienteService:
    def __init__(self):
        self.listCliente = load_json('data/listcliente.json')

    def menu(self):
        while True:
            options = ["Listar Clientes", "Adicionar Cliente", "Atualizar Cliente", "Remover Cliente", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.listaClientes()
            elif choice == 1:
                self.adicionaCliente()
            elif choice == 2:
                self.atualizaCliente()
            elif choice == 3:
                self.removeCliente()
            elif choice == 4:
                break

    def listaClientes(self):
        for item in self.listCliente:
            print(item)
 
    def adicionaCliente(self):
        # Encontrar o maior ID existente
        maiorID = max([cliente['id'] for cliente in self.listCliente], default=0)
        novoID = maiorID + 1

        nome = input("Nome: ")
        
        # Verificar se o NIF já existe
        while True:
            try:
                nif = int(input("Introduz um NIF: "))
            except IOError as e:
                print("An error occurred:", e)
            if any(cliente['nif'] == nif for cliente in self.listCliente):
                print("Erro: Este NIF já está cadastrado para outro cliente.")
            else:
                break
  
        dataNascimento = input("Data de Nascimento: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        
        novo_cliente = Cliente(novoID, nome, nif, dataNascimento, telefone, email)
        self.listCliente.append(novo_cliente.__dict__)
        self.guardaAlteracoesCliente()
        print(f"Cliente adicionado com sucesso. ID atribuído: {novoID}")

    def atualizaCliente(self):
        try:
            id = int(input("ID do cliente a atualizar: "))
        except IOError as e:
            print("Ocorreu um erro ao introduzir o ID cliente:", e)
            
        
        for cliente in self.listCliente:
            if cliente['id'] == id:
                cliente['nome'] = input("Novo Nome: ") or cliente['nome']
                
                # Verificar se o novo NIF já existe para outro cliente
                while True:
                    try:
                        novofNIF = int(input("Novo NIF: ") or cliente['nif'])
                    except IOError as e:
                        print("Ocorreu um erro ao introduzir o NIF:", e)
                        
                    if novofNIF != cliente['nif'] and any(c['nif'] == novofNIF for c in self.listCliente):
                        print("Erro: Este NIF já está cadastrado para outro cliente.")
                    else:
                        cliente['nif'] = novofNIF
                        break
                
                cliente['dataNascimento'] = input("Nova Data de Nascimento: ") or cliente['dataNascimento']
                cliente['telefone'] = input("Novo Telefone: ") or cliente['telefone']
                cliente['email'] = input("Novo Email: ") or cliente['email']
                self.guardaAlteracoesCliente()
                print("Cliente atualizado com sucesso.")
                return
        print("Cliente não encontrado.")

    def removeCliente(self):
        try:    
            id = int(input("ID do cliente a remover: "))
        except IOError as e:
            print("Ocorreu um erro ao introduzir o ID cliente:", e)
        
        self.listCliente = [cliente for cliente in self.listCliente if cliente['id'] != id]
        self.guardaAlteracoesCliente()

    def guardaAlteracoesCliente(self):
        save_json('data/listcliente.json', self.listCliente)
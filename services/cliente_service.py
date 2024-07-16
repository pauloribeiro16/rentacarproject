from utils.generalfunctions import load_json, save_json, maiorIDLista, verificaIDInteiro, selecionaData
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
        try:
            novoID = maiorIDLista(self.listCliente) + 1
            nome = self.validaNoneNullInput("Nome: ")

            nif = self.validaNif()
            dataNascimento = selecionaData("Data de Nascimento: ")
            telefone = self.validaTelefone()
            email = self.validaEmail()

            novo_cliente = Cliente(novoID, nome, nif, dataNascimento, telefone, email)
            self.listCliente.append(novo_cliente.__dict__)
            self.guardaAlteracoesCliente()
            print(f"Cliente adicionado com sucesso. ID atribuído: {novoID}")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao adicionar o cliente: {e}")

    def atualizaCliente(self):
        try:
            id = verificaIDInteiro(self, "ID do cliente a atualizar: ")
            cliente = next((c for c in self.listCliente if c['id'] == id), None)
            if cliente:
                cliente['nome'] = self.validaNoneNullInput("Novo Nome: ", optional=True) or cliente['nome']
                cliente['nif'] = self.validaNif(cliente['nif'])
                cliente['dataNascimento'] = selecionaData("Nova Data de Nascimento: ", optional=True) or cliente['dataNascimento']
                cliente['telefone'] = self.validaTelefone(cliente['telefone'])
                cliente['email'] = self.validaEmail(cliente['email'])
                self.guardaAlteracoesCliente()
                print("Cliente atualizado com sucesso.")
            else:
                print("Cliente não encontrado.")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao atualizar o cliente: {e}")

    def removeCliente(self):
        try:
            cliente_options = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
            cliente_choice = beaupy.select(cliente_options, cursor='->', cursor_style='red', return_index=True)
            cliente = self.listCliente[cliente_choice]
            
            confirm = self.validaConfirmacao(f"Tem certeza que deseja remover o cliente {cliente['nome']} (ID: {cliente['id']})? (S/N): ")
            if confirm == 'S':
                self.listCliente = [c for c in self.listCliente if c['id'] != cliente['id']]
                self.guardaAlteracoesCliente()
                print("Cliente removido com sucesso.")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao remover o cliente: {e}")

    def guardaAlteracoesCliente(self):
        save_json('data/listcliente.json', self.listCliente)

    def validaNoneNullInput(self, valor, optional=False):
        while True:
            value = input(valor)
            if optional and not value:
                return None
            if value:
                return value
            print("Este campo não pode estar vazio.")

    def validaNif(self, current_nif=None):
        while True:
            try:
                nif = int(input("NIF: ") if current_nif is None else input(f"Novo NIF ({current_nif}): ") or current_nif)
                if nif != current_nif and any(cliente['nif'] == nif for cliente in self.listCliente):
                    print("Erro: Este NIF já está cadastrado para outro cliente.")
                else:
                    return nif
            except ValueError:
                print("Por favor, insira um NIF válido.")

    def validaTelefone(self, current_telefone=None):
        while True:
            telefone = input("Telefone: ") if current_telefone is None else input(f"Novo Telefone ({current_telefone}): ") or current_telefone
            if telefone != current_telefone and any(cliente['telefone'] == telefone for cliente in self.listCliente):
                print("Erro: Este telefone já está cadastrado para outro cliente.")
            else:
                return telefone

    def validaEmail(self, current_email=None):
        while True:
            email = input("Email: ") if current_email is None else input(f"Novo Email ({current_email}): ") or current_email
            if email != current_email and any(cliente['email'] == email for cliente in self.listCliente):
                print("Erro: Este email já está cadastrado para outro cliente.")
            else:
                return email


    def validaConfirmacao(self, valor):
        while True:
            resposta = input(valor).strip().upper()
            if resposta in ['S', 'N']:
                return resposta
            print("Resposta inválida. Por favor, insira 'S' para sim ou 'N' para não.")

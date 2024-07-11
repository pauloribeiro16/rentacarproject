from utils.json_utils import load_json, save_json, validaMatricula, maiorIDLista, verificaIDInteiro
from models.automovel import Automovel
import beaupy


class AutomovelService:
    def __init__(self):
        self.listAutomovel = load_json('data/listautomovel.json')

    def menu(self):
        while True:
            options = ["Listar Automóveis", "Adicionar Automóvel", "Atualizar Automóvel", "Remover Automóvel", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.listaAutomoveis()
            elif choice == 1:
                self.adicionaAutomovel()
            elif choice == 2:
                self.atualizaAutomovel()
            elif choice == 3:
                self.removeAutomovel()
            elif choice == 4:
                break

    def listaAutomoveis(self):
        for item in self.listAutomovel:
            print(item)

    def adicionaAutomovel(self):
        try:
            novoID = maiorIDLista(self.listAutomovel) + 1
            matricula = self.verificaMatricula()
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            cor = input("Cor: ")
            portas = verificaIDInteiro(self,"Portas: ")
            precoDiario = self.verificaFloat("Preço Diário: ")
            cilindrada = verificaIDInteiro(self,"Cilindrada: ")
            potencia = verificaIDInteiro(self,"Potência: ")

            novo_automovel = Automovel(novoID, matricula, marca, modelo, cor, portas, precoDiario, cilindrada, potencia)
            self.listAutomovel.append(novo_automovel.__dict__)
            self.guardaAlteracoes()
            print("Automóvel adicionado com sucesso!")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao adicionar o automóvel: {e}")

    def atualizaAutomovel(self):
        try:
            id = verificaIDInteiro(self,"ID do automóvel a atualizar: ")
            for automovel in self.listAutomovel:
                if automovel['id'] == id:
                    automovel['matricula'] = self.verificaMatricula(optional=True) or automovel['matricula']
                    automovel['marca'] = input("Nova Marca: ") or automovel['marca']
                    automovel['modelo'] = input("Novo Modelo: ") or automovel['modelo']
                    automovel['cor'] = input("Nova Cor: ") or automovel['cor']
                    automovel['portas'] = verificaIDInteiro(self,"Novas Portas: ") or automovel['portas']
                    automovel['precoDiario'] = self.verificaFloat("Novo Preço Diário: ") or automovel['precoDiario']
                    automovel['cilindrada'] = verificaIDInteiro(self,"Nova Cilindrada: ") or automovel['cilindrada']
                    automovel['potencia'] = verificaIDInteiro(self,"Nova Potência: ") or automovel['potencia']
                    self.guardaAlteracoes()
                    print("Automóvel atualizado com sucesso!")
                    return
            print("Automóvel não encontrado.")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao atualizar o automóvel: {e}")

    def removeAutomovel(self):
        try:
            id = verificaIDInteiro(self,"ID do automóvel a remover: ")
            self.listAutomovel = [automovel for automovel in self.listAutomovel if automovel['id'] != id]
            self.guardaAlteracoes()
            print("Automóvel removido com sucesso!")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao remover o automóvel: {e}")

    def guardaAlteracoes(self):
        save_json('data/listautomovel.json', self.listAutomovel)

    def verificaFloat(self, valor, optional=False):
        while True:
            try:
                value = input(valor)
                if optional and not value:
                    return None
                return float(value)
            except ValueError:
                print("Por favor, insira um número decimal válido.")

    def verificaMatricula(self, optional=False):
        while True:
            try:
                matricula = input("Matrícula (XX-XX-XX): ")
                if optional and not matricula:
                    return None
                return validaMatricula(matricula)
            except ValueError as e:
                print(f"Erro: {e}")


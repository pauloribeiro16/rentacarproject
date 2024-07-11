from utils.json_utils import load_json, save_json
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
        
        maiorID = max([automovel['id'] for automovel in self.listAutomovel], default=0)
        novoID = maiorID + 1

        try:
            matricula = input("Matrícula: ")
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            cor = input("Cor: ")
            portas = int(input("Portas: "))
            precoDiario = float(input("Preço Diário: "))
            cilindrada = int(input("Cilindrada: "))
            potencia = int(input("Potência: "))

            novo_automovel = Automovel(novoID, matricula, marca, modelo, cor, portas, precoDiario, cilindrada, potencia)
            self.listAutomovel.append(novo_automovel.__dict__)
            self.guardaAlteracaoes()
        except IOError as e:
            print("Ocorreu um erro ao introduzir ao adicionar o automovel:", e)
        

    def atualizaAutomovel(self):
        try:
            id = int(input("ID do automóvel a atualizar: "))
            for automovel in self.listAutomovel:
                if automovel['id'] == id:
                    automovel['matricula'] = input("Nova Matrícula: ") or automovel['matricula']
                    automovel['marca'] = input("Nova Marca: ") or automovel['marca']
                    automovel['modelo'] = input("Novo Modelo: ") or automovel['modelo']
                    automovel['cor'] = input("Nova Cor: ") or automovel['cor']
                    automovel['portas'] = int(input("Novas Portas: ") or automovel['portas'])
                    automovel['precoDiario'] = float(input("Novo Preço Diário: ") or automovel['precoDiario'])
                    automovel['cilindrada'] = int(input("Nova Cilindrada: ") or automovel['cilindrada'])
                    automovel['potencia'] = int(input("Nova Potência: ") or automovel['potencia'])
                    self.guardaAlteracaoes()
                    return
            print("Automóvel não encontrado.")
        except IOError as e:
            print("Ocorreu um erro ao atualizar automovel", e)

    def removeAutomovel(self):
        try:
            id = int(input("ID do automóvel a remover: "))
            self.listAutomovel = [automovel for automovel in self.listAutomovel if automovel['id'] != id]
            self.guardaAlteracaoes()
        except IOError as e:
            print("Ocorreu um erro ao remover o automovel", e)
            

    def guardaAlteracaoes(self):
        save_json('data/listautomovel.json', self.listAutomovel)

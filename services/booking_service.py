from utils.json_utils import load_json, save_json
from models.booking import Booking
import beaupy
import datetime

class BookingService:
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')

    def menu(self):
        while True:
            options = ["Listar Reservas", "Adicionar Reserva", "Atualizar Reserva", "Remover Reserva", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.listaBookings()
            elif choice == 1:
                self.adicionaBookings()
            elif choice == 2:
                self.atualizaBookings()
            elif choice == 3:
                self.removeBooking()
            elif choice == 4:
                break

    def listaBookings(self):
        for item in self.listBooking:
            print(item)

    def adicionaBookings(self):
        try:
            data_inicio = input("Data Início (YYYY-MM-DD): ")
            data_fim = input("Data Fim (YYYY-MM-DD): ")
            cliente_id = int(input("ID do Cliente: "))
            automovel_id = int(input("ID do Automóvel: "))
            
            # Calcula o número de dias da reserva
            numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
            
            # Calcula o preço da reserva
            precoReserva = self.calculaPreco(automovel_id, numeroDias)
            
            # Cria o objeto de reserva
            nova_reserva = {
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "cliente_id": cliente_id,
                "automovel_id": automovel_id,
                "precoReserva": precoReserva,
                "numeroDias": numeroDias
            }
            
            # Verifica disponibilidade
            if self.verificaDisponibilidade(automovel_id, data_inicio, data_fim):
                self.listBooking.append(nova_reserva)
                self.guardaAlteracoesBooking()
                print("Reserva adicionada com sucesso!")
            else:
                print("Este automóvel não está disponível para as datas especificadas.")
        
        except ValueError as e:
            print(f"Erro ao adicionar reserva: {e}")

    def verificaDisponibilidade(self, automovel_id, data_inicio, data_fim):
        for reserva in self.listBooking:
            if reserva["automovel_id"] == automovel_id:
                if (data_inicio >= reserva["data_inicio"] and data_inicio <= reserva["data_fim"]) or \
                   (data_fim >= reserva["data_inicio"] and data_fim <= reserva["data_fim"]) or \
                   (data_inicio <= reserva["data_inicio"] and data_fim >= reserva["data_fim"]):
                    return False  # Há sobreposição de datas
        return True  # Não há sobreposição de datas, o automóvel está disponível

    def atualizaBookings(self):
        id = int(input("ID do cliente a atualizar: "))
        for cliente in self.listCliente:
            if cliente['id'] == id:
                cliente['nome'] = input("Novo Nome: ") or cliente['nome']
                cliente['nif'] = int(input("Novo NIF: ") or cliente['nif']) # função para verificar id
                cliente['dataNascimento'] = input("Nova Data de Nascimento: ") or cliente['dataNascimento']
                cliente['telefone'] = input("Novo Telefone: ") or cliente['telefone']
                cliente['email'] = input("Novo Email: ") or cliente['email']
                self.guardaAlteracoesBooking()
                return
        print("Cliente não encontrado.")


    def removeBooking(self):
        id = int(input("ID da reserva a remover: "))
        self.listBooking = [booking for booking in self.listBooking if booking['id'] != id]
        self.guardaAlteracoesBooking()

    def calculaPreco(self, automovel_id, numeroDias):
        for automovel in load_json('data/listautomovel.json'):
            if automovel['id'] == automovel_id:
                return automovel['precoDiario'] * numeroDias
        return 0

    def guardaAlteracoesBooking(self):
        save_json('data/listbooking.json', self.listBooking)

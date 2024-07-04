from utils.json_utils import load_json, save_json
from models.booking import Booking
import beaupy
import datetime

class BookingService:
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')

    def manage(self):
        while True:
            options = ["Listar Reservas", "Adicionar Reserva", "Atualizar Reserva", "Remover Reserva", "Voltar"]
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
        for item in self.listBooking:
            print(item)

    def add_item(self):
        data_inicio = input("Data Início (YYYY-MM-DD): ")
        data_fim = input("Data Fim (YYYY-MM-DD): ")
        cliente_id = int(input("ID do Cliente: "))
        automovel_id = int(input("ID do Automóvel: "))
        numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
        precoReserva = self.calculate_price(automovel_id, numeroDias)
        nova_reserva = Booking(data_inicio, data_fim, cliente_id, automovel_id, precoReserva, numeroDias)
        self.listBooking.append(nova_reserva.__dict__)
        self.save_changes()

    def update_item(self):
        # Implementar a lógica para atualizar uma reserva existente
        pass

    def remove_item(self):
        id = int(input("ID da reserva a remover: "))
        self.listBooking = [booking for booking in self.listBooking if booking['id'] != id]
        self.save_changes()

    def calculate_price(self, automovel_id, numeroDias):
        for automovel in load_json('data/listautomovel.json'):
            if automovel['id'] == automovel_id:
                return automovel['precoDiario'] * numeroDias
        return 0

    def save_changes(self):
        save_json('data/listbooking.json', self.listBooking)

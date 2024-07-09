import sys
import os
import datetime
import beaupy
from utils.json_utils import load_json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class PesquisasService:
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')
        self.listCliente = load_json('data/listcliente.json')
        self.listAutomovel = load_json('data/listautomovel.json')

    def manage(self):
        while True:
            options = ["Pesquisa por Cliente", "Pesquisa por Matrícula", "Listagem de Bookings Futuros", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                try:    
                    nif = int(input("Introduza um NIF válido: "))
                    self.pesquisar_cliente_por_nif(self.listCliente, self.listBooking, nif)
                except ValueError:
                    print("NIF inválido.")
            elif choice == 1:
                try:    
                    matricula = input("Introduza uma matrícula válida: ")
                    self.pesquisaPorMatricula(self.listAutomovel, self.listBooking, matricula)
                except ValueError:
                    print("Matrícula inválida.")
            elif choice == 2:
                self.listarBookingsFuturos(self.listBooking, self.listCliente, self.listAutomovel)
            elif choice == 3:
                break

    def pesquisar_cliente_por_nif(self, listCliente, listBooking, nif):
        cliente = next((c for c in listCliente if c['nif'] == nif), None)
        if cliente:
            print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, NIF: {cliente['nif']}, Telefone: {cliente['telefone']}, Email: {cliente['email']}")
            ultimos_alugueres = [b for b in listBooking if b['cliente_id'] == cliente['id']][-5:]
            for booking in ultimos_alugueres:
                total_com_desconto = self.aplicar_desconto(booking['numeroDias'], booking['precoReserva'])
                print(f"Reserva de {booking['data_inicio']} a {booking['data_fim']} ({booking['numeroDias']} dias) - Total: {total_com_desconto:.2f}€")
        else:
            print("Cliente não encontrado.")

    def pesquisaPorMatricula(self, listAutomovel, listBooking, matricula):
        automovel = next((a for a in listAutomovel if a['matricula'] == matricula), None)
        if automovel:
            print(f"ID: {automovel['id']}, Marca: {automovel['marca']}, Modelo: {automovel['modelo']}, Cor: {automovel['cor']}, Portas: {automovel['portas']}, Preço Diário: {automovel['precoDiario']}€")
            ultimos_alugueres = [b for b in listBooking if b['automovel_id'] == automovel['id']][-5:]
            for booking in ultimos_alugueres:
                total_com_desconto = self.aplicar_desconto(booking['numeroDias'], booking['precoReserva'])
                print(f"Reserva de {booking['data_inicio']} a {booking['data_fim']} ({booking['numeroDias']} dias) - Total: {total_com_desconto:.2f}€")
        else:
            print("Automóvel não encontrado.")

    def listarBookingsFuturos(self, listBooking, listCliente, listAutomovel):
        hoje = datetime.datetime.today().date()
        for booking in listBooking:
            data_inicio = datetime.datetime.strptime(booking['data_inicio'], '%Y-%m-%d').date()
            if data_inicio >= hoje:
                cliente = next((c for c in listCliente if c['id'] == booking['cliente_id']), None)
                automovel = next((a for a in listAutomovel if a['id'] == booking['automovel_id']), None)
                if cliente and automovel:
                    total_com_desconto = self.aplicar_desconto(booking['numeroDias'], booking['precoReserva'])
                    print(f"Booking data início: {booking['data_inicio']} | data fim: {booking['data_fim']} ({booking['numeroDias']} dias)")
                    print(f"Cliente: {cliente['nome']}")
                    print(f"Automóvel: {automovel['marca']} – Matrícula: {automovel['matricula']}")
                    print(f"Total: {total_com_desconto:.2f}€\n")

    def aplicar_desconto(self, numero_dias, preco_reserva):
        if numero_dias <= 4:
            desconto = 0
        elif 5 <= numero_dias <= 8:
            desconto = 0.15
        else:
            desconto = 0.25
        return preco_reserva * (1 - desconto)

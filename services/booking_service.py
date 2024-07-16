from utils.generalfunctions import load_json, save_json, validaData
from datetime import datetime
import re
import matplotlib.pyplot as plt
import beaupy

class BookingService:
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')
        self.listAutomovel = load_json('data/listautomovel.json')
        self.listCliente = load_json('data/listcliente.json')

    def menu(self):
        while True:
            options = ["Listar Reservas", "Adicionar Reserva", "Atualizar Reserva", "Remover Reserva" "Voltar"]
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
            # Obter e validar data de início
            while True:
                try:
                    data_inicio = validaData(input("Data Início (YYYY-MM-DD): "))
                    break
                except ValueError as e:
                    print(f"Erro: {e}")

            # Obter e validar data de fim
            while True:
                try:
                    data_fim = validaData(input("Data Fim (YYYY-MM-DD): "))
                    if datetime.strptime(data_fim, '%Y-%m-%d') <= datetime.strptime(data_inicio, '%Y-%m-%d'):
                        raise ValueError("A data de fim deve ser posterior à data de início.")
                    break
                except ValueError as e:
                    print(f"Erro: {e}")

            # Selecionar cliente
            cliente_options = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
            cliente_choice = beaupy.select(cliente_options, cursor='->', cursor_style='red', return_index=True)
            cliente_id = self.listCliente[cliente_choice]['id']

            # Selecionar automóvel
            automovel_options = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in self.listAutomovel]
            automovel_choice = beaupy.select(automovel_options, cursor='->', cursor_style='red', return_index=True)
            automovel_id = self.listAutomovel[automovel_choice]['id']
            
            # Calcula o número de dias da reserva
            numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
            
            # Calcula o preço da reserva
            precoReserva = self.calculaPreco(automovel_id, numeroDias)
            
            # Aplica descontos no preço da reserva
            precoFinal = self.AplicaDescontos(numeroDias, precoReserva)
            
            # Cria o objeto de reserva
            nova_reserva = {
                "id": self.geraNovoID(self.listBooking),
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "cliente_id": cliente_id,
                "automovel_id": automovel_id,
                "precoReserva": precoFinal,
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
        try:
            id = int(input("ID da reserva a atualizar: "))
        except ValueError as e:
            print(f"Erro ao introduzir ID Booling: {e}")

        for booking in self.listBooking:
            if booking['id'] == id:
                try:
                    booking['data_inicio'] = input(f"Nova Data Início ({booking['data_inicio']}): ") or booking['data_inicio']
                    booking['data_fim'] = input(f"Nova Data Fim ({booking['data_fim']}): ") or booking['data_fim']

                    # Selecionar novo cliente
                    cliente_options = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
                    cliente_choice = beaupy.select(cliente_options, cursor='->', cursor_style='red', return_index=True)
                    booking['cliente_id'] = self.listCliente[cliente_choice]['id']

                    # Selecionar novo automóvel
                    automovel_options = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in self.listAutomovel]
                    automovel_choice = beaupy.select(automovel_options, cursor='->', cursor_style='red', return_index=True)
                    booking['automovel_id'] = self.listAutomovel[automovel_choice]['id']

                    # Recalcula o número de dias da reserva
                    numeroDias = (datetime.strptime(booking['data_fim'], '%Y-%m-%d') - datetime.strptime(booking['data_inicio'], '%Y-%m-%d')).days
                except ValueError as e:
                    print(f"Erro valores nna reserva: {e}")

                # Recalcula o preço da reserva
                booking['precoReserva'] = self.calculaPreco(booking['automovel_id'], numeroDias)
                
                # Aplica descontos no preço recalculado da reserva
                booking['precoReserva'] = self.AplicaDescontos(numeroDias, booking['precoReserva'])
                
                self.guardaAlteracoesBooking()
                return
        print("Reserva não encontrada.")

    def removeBooking(self):
        try:
            id = int(input("ID da reserva a remover: "))
            self.listBooking = [booking for booking in self.listBooking if booking['id'] != id]
            self.guardaAlteracoesBooking()
        except ValueError as e:
                    print(f"Erro valores ao reserva: {e}")

    def calculaPreco(self, automovel_id, numeroDias):
        for automovel in self.listAutomovel:
            if automovel['id'] == automovel_id:
                return automovel['precoDiario'] * numeroDias
        return 0
    
    def AplicaDescontos(self, numeroDias, precoReserva):
        if numeroDias <= 4:
            desconto = 0
        elif 5 <= numeroDias <= 8:
            desconto = 0.15
        elif numeroDias >=9:
            desconto = 0.25
        return precoReserva * (1 - desconto)

    def guardaAlteracoesBooking(self):
        save_json('data/listbooking.json', self.listBooking)

    def geraNovoID(self, lista):
        if not lista:
            return 1
        return max(item["id"] for item in lista) + 1

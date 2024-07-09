from utils.json_utils import load_json, save_json
from datetime import datetime
import re
import beaupy

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
            # Função para validar o formato da data
            def validar_data(data_str):
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', data_str):
                    raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")
                datetime.strptime(data_str, '%Y-%m-%d')  # Verifica se a data é válida
                return data_str

            # Obter e validar data de início
            while True:
                try:
                    data_inicio = validar_data(input("Data Início (YYYY-MM-DD): "))
                    break
                except ValueError as e:
                    print(f"Erro: {e}")

            # Obter e validar data de fim
            while True:
                try:
                    data_fim = validar_data(input("Data Fim (YYYY-MM-DD): "))
                    if datetime.strptime(data_fim, '%Y-%m-%d') <= datetime.strptime(data_inicio, '%Y-%m-%d'):
                        raise ValueError("A data de fim deve ser posterior à data de início.")
                    break
                except ValueError as e:
                    print(f"Erro: {e}")

            cliente_id = int(input("ID do Cliente: "))
            automovel_id = int(input("ID do Automóvel: "))
            
            # Calcula o número de dias da reserva
            numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
            
            # Calcula o preço da reserva
            precoReserva = self.calculaPreco(automovel_id, numeroDias)
            
            # Aplica descontos no preço da reserva
            precoFinal = self.AplicaDescontos(numeroDias, precoReserva)
            
            # Cria o objeto de reserva
            nova_reserva = {
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
        id = int(input("ID da reserva a atualizar: "))
        for booking in self.listBooking:
            if booking['id'] == id:
                booking['data_inicio'] = input(f"Nova Data Início ({booking['data_inicio']}): ") or booking['data_inicio']
                booking['data_fim'] = input(f"Nova Data Fim ({booking['data_fim']}): ") or booking['data_fim']
                booking['cliente_id'] = int(input(f"Novo ID do Cliente ({booking['cliente_id']}): ") or booking['cliente_id'])
                booking['automovel_id'] = int(input(f"Novo ID do Automóvel ({booking['automovel_id']}): ") or booking['automovel_id'])
                
                # Recalcula o número de dias da reserva
                numeroDias = (datetime.strptime(booking['data_fim'], '%Y-%m-%d') - datetime.strptime(booking['data_inicio'], '%Y-%m-%d')).days
                
                # Recalcula o preço da reserva
                booking['precoReserva'] = self.calculaPreco(booking['automovel_id'], numeroDias)
                
                # Aplica descontos no preço recalculado da reserva
                booking['precoReserva'] = self.AplicaDescontos(numeroDias, booking['precoReserva'])
                
                self.guardaAlteracoesBooking()
                return
        print("Reserva não encontrada.")

    def removeBooking(self):
        id = int(input("ID da reserva a remover: "))
        self.listBooking = [booking for booking in self.listBooking if booking['id'] != id]
        self.guardaAlteracoesBooking()

    def calculaPreco(self, automovel_id, numeroDias):
        for automovel in load_json('data/listautomovel.json'):
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

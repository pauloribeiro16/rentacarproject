from utils.json_utils import load_json, save_json, validaData, maiorIDLista, verificaIDInteiro
from datetime import datetime
import beaupy

class BookingService:
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')
        self.listAutomovel = load_json('data/listautomovel.json')
        self.listCliente = load_json('data/listcliente.json')

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
            data_inicio = self.verificaData("Data Início (YYYY-MM-DD): ")
            data_fim = self.verificaData("Data Fim (YYYY-MM-DD): ", data_inicio)
            cliente_id = self.verificaIDExisteLista("ID do Cliente: ", self.listCliente)
            automovel_id = self.verificaIDExisteLista("ID do Automóvel: ", self.listAutomovel)

            if not self.verificaDisponibilidade(automovel_id, data_inicio, data_fim):
                print("Este automóvel não está disponível para as datas especificadas.")
                return

            numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
            precoReserva = self.calculaPreco(automovel_id, numeroDias)
            precoFinal = self.AplicaDescontos(numeroDias, precoReserva)

            nova_reserva = {
                "id": maiorIDLista(self.listBooking)+1,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "cliente_id": cliente_id,
                "automovel_id": automovel_id,
                "precoReserva": precoFinal,
                "numeroDias": numeroDias
            }

            self.listBooking.append(nova_reserva)
            self.guardaAlteracoesBooking()
            print("Reserva adicionada com sucesso!")
        except ValueError as e:
            print(f"Erro ao adicionar reserva: {e}")

    def verificaDisponibilidade(self, automovel_id, data_inicio, data_fim, reserva_id=None):
        for reserva in self.listBooking:
            if reserva["automovel_id"] == automovel_id and reserva["id"] != reserva_id:
                if (data_inicio >= reserva["data_inicio"] and data_inicio <= reserva["data_fim"]) or \
                   (data_fim >= reserva["data_inicio"] and data_fim <= reserva["data_fim"]) or \
                   (data_inicio <= reserva["data_inicio"] and data_fim >= reserva["data_fim"]):
                    return False  # Há sobreposição de datas
        return True  # Não há sobreposição de datas, o automóvel está disponível

    def atualizaBookings(self):
        try:
            id = verificaIDInteiro(self,"ID da reserva a atualizar: ")
            for booking in self.listBooking:
                if booking['id'] == id:
                    try:
                        data_inicio = self.verificaData(f"Nova Data Início ({booking['data_inicio']}): ") or booking['data_inicio']
                        data_fim = self.verificaData(f"Nova Data Fim ({booking['data_fim']}): ", data_inicio) or booking['data_fim']
                        cliente_id = self.verificaIDExisteLista(f"Novo ID do Cliente ({booking['cliente_id']}): ", self.listCliente) or booking['cliente_id']
                        automovel_id = self.verificaIDExisteLista(f"Novo ID do Automóvel ({booking['automovel_id']}): ", self.listAutomovel) or booking['automovel_id']

                        if not self.verificaDisponibilidade(automovel_id, data_inicio, data_fim, id):
                            print("Este automóvel não está disponível para as datas especificadas.")
                            return

                        numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
                        precoReserva = self.calculaPreco(automovel_id, numeroDias)
                        precoFinal = self.AplicaDescontos(numeroDias, precoReserva)

                        booking.update({
                            'data_inicio': data_inicio,
                            'data_fim': data_fim,
                            'cliente_id': cliente_id,
                            'automovel_id': automovel_id,
                            'precoReserva': precoFinal,
                            'numeroDias': numeroDias
                        })

                        self.guardaAlteracoesBooking()
                        print("Reserva atualizada com sucesso!")
                        return
                    except ValueError as e:
                        print(f"Erro ao atualizar valores da reserva: {e}")
            print("Reserva não encontrada.")
        except ValueError as e:
            print(f"Erro ao introduzir ID da reserva: {e}")

    def removeBooking(self):
        try:
            id = verificaIDInteiro(self,"ID da reserva a remover: ")
            self.listBooking = [booking for booking in self.listBooking if booking['id'] != id]
            self.guardaAlteracoesBooking()
            print("Reserva removida com sucesso!")
        except ValueError as e:
            print(f"Erro ao remover reserva: {e}")

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
        elif numeroDias >= 9:
            desconto = 0.25
        return precoReserva * (1 - desconto)

    def guardaAlteracoesBooking(self):
        save_json('data/listbooking.json', self.listBooking)

    def verificaData(self, valor, start_date=None):
        while True:
            try:
                date_str = input(valor)
                date = validaData(date_str)
                if start_date and datetime.strptime(date, '%Y-%m-%d') <= datetime.strptime(start_date, '%Y-%m-%d'):
                    raise ValueError("A data de fim deve ser posterior à data de início.")
                return date
            except ValueError as e:
                print(f"Erro: {e}")

    def verificaIDExisteLista(self, valor, lista):
        while True:
            try:
                id = int(input(valor))
                if any(item['id'] == id for item in lista):
                    return id
                else:
                    print("ID não encontrado. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número inteiro válido.")

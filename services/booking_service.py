from utils.generalfunctions import load_json, save_json, validaData, selecionaData, validaConfirmacao, maiorIDLista
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
        print("\n=== Lista de Reservas ===")
        for booking in self.listBooking:
            cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
            automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
            
            print(f"ID da Reserva: {booking['id']}")
            print(f"Data de Início: {booking['data_inicio']}")
            print(f"Data de Fim: {booking['data_fim']}")
            print(f"Cliente: {cliente['nome']}")
            print(f"Automóvel: {automovel['marca']} {automovel['modelo']}")
            print(f"Preço da Reserva: €{booking['precoReserva']:.2f}")
            print(f"Número de Dias: {booking['numeroDias']}")
            print("-" * 30)

    def adicionaBookings(self):
        try:
            data_inicio = selecionaData("Selecionar Data de Início")
            data_fim = selecionaData("Selecionar Data de Fim")
            if datetime.strptime(data_fim, '%Y-%m-%d') <= datetime.strptime(data_inicio, '%Y-%m-%d'):
                raise ValueError("A data de fim deve ser posterior à data de início.")

            cliente_options = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
            cliente_choice = beaupy.select(cliente_options, cursor='->', cursor_style='red', return_index=True)
            cliente_id = self.listCliente[cliente_choice]['id']

            opcoesAutomovel = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in self.listAutomovel]
            automovel_choice = beaupy.select(opcoesAutomovel, cursor='->', cursor_style='red', return_index=True)
            automovel_id = self.listAutomovel[automovel_choice]['id']
            
            numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
            precoReserva = self.calculaPreco(automovel_id, numeroDias)
            precoFinal = self.AplicaDescontos(numeroDias, precoReserva)
            
            novaReserva = {
                "id": maiorIDLista(self.listBooking)+1,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "cliente_id": cliente_id,
                "automovel_id": automovel_id,
                "precoReserva": precoFinal,
                "numeroDias": numeroDias
            }
            
            if self.verificaDisponibilidade(automovel_id, data_inicio, data_fim):
                self.listBooking.append(novaReserva)
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
            print(f"Erro ao introduzir ID da reserva: {e}")
            return

        for booking in self.listBooking:
            if booking['id'] == id:
                try:
                    booking['data_inicio'] = selecionaData(f"Nova Data Início ({booking['data_inicio']}): ") or booking['data_inicio']
                    booking['data_fim'] = selecionaData(f"Nova Data Fim ({booking['data_fim']}): ") or booking['data_fim']

                    cliente_options = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
                    cliente_choice = beaupy.select(cliente_options, cursor='->', cursor_style='red', return_index=True)
                    booking['cliente_id'] = self.listCliente[cliente_choice]['id']

                    opcoesAutomovel = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in self.listAutomovel]
                    automovel_choice = beaupy.select(opcoesAutomovel, cursor='->', cursor_style='red', return_index=True)
                    booking['automovel_id'] = self.listAutomovel[automovel_choice]['id']

                    numeroDias = (datetime.strptime(booking['data_fim'], '%Y-%m-%d') - datetime.strptime(booking['data_inicio'], '%Y-%m-%d')).days
                    booking['precoReserva'] = self.calculaPreco(booking['automovel_id'], numeroDias)
                    booking['precoReserva'] = self.AplicaDescontos(numeroDias, booking['precoReserva'])
                    
                    self.guardaAlteracoesBooking()
                    print("Reserva atualizada com sucesso.")
                    return
                except ValueError as e:
                    print(f"Erro ao atualizar a reserva: {e}")
                    return
        print("Reserva não encontrada.")

    def removeBooking(self):
        try:
            booking_options = []
            for booking in self.listBooking:
                cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
                automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
                
                if cliente and automovel:
                    option = f"Data inicio: {booking['data_inicio']} Data fim: {booking['data_fim']} Cliente: {cliente['nome']} Automovel: {automovel['marca']} {automovel['modelo']}"
                    booking_options.append(option)
            
            escolhaBooking = beaupy.select(booking_options, cursor='->', cursor_style='red', return_index=True)
            booking = self.listBooking[escolhaBooking]
            
            cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
            automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
            
            mensagemConfirmacao = f"Tem certeza que deseja remover a reserva?\n"
            mensagemConfirmacao += f"Data inicio: {booking['data_inicio']}\n"
            mensagemConfirmacao += f"Data fim: {booking['data_fim']}\n"
            mensagemConfirmacao += f"Cliente: {cliente['nome']}\n"
            mensagemConfirmacao += f"Automovel: {automovel['marca']} {automovel['modelo']}\n"
            mensagemConfirmacao += "(S/N): "
            
            confirm = validaConfirmacao(mensagemConfirmacao)
            if confirm == 'S':
                self.listBooking.remove(booking)
                self.guardaAlteracoesBooking()
                print("Reserva removida com sucesso.")
            else:
                print("Operação cancelada.")
        
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
        elif numeroDias >=9:
            desconto = 0.25
        return precoReserva * (1 - desconto)

    def guardaAlteracoesBooking(self):
        save_json('data/listbooking.json', self.listBooking)

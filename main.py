from services.automovel_service import AutomovelService
from services.cliente_service import ClienteService
from services.booking_service import BookingService
from services.pesquisas_service import PesquisasService
import beaupy

def main_menu():
    options = ["Gerir Automóveis", "Gerir Clientes", "Gerir Reservas", "Pesquisas", "Sair"]
    choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
    return choice

def main():
    automovel_service = AutomovelService()
    cliente_service = ClienteService()
    booking_service = BookingService()
    pesquisas_service = PesquisasService()

    while True:
        choice = main_menu()
        if choice == 0:
            automovel_service.menu()
        elif choice == 1:
            cliente_service.menu()
        elif choice == 2:
            booking_service.menu()
        elif choice == 3:
            pesquisas_service.menu()
        elif choice == 4:
            break

main()

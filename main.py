from services.automovel_service import AutomovelService
from services.cliente_service import ClienteService
from services.booking_service import BookingService
import beaupy

def main_menu():
    options = ["Gerir Automóveis", "Gerir Clientes", "Gerir Reservas", "Sair"]
    choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
    return choice

def main():
    automovel_service = AutomovelService()
    cliente_service = ClienteService()
    booking_service = BookingService()

    while True:
        choice = main_menu()
        if choice == 0:
            automovel_service.manage()
        elif choice == 1:
            cliente_service.manage()
        elif choice == 2:
            booking_service.manage()
        elif choice == 3:
            break

if __name__ == "__main__":
    main()
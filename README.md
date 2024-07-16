# Rent-A-Car Management System

Welcome to the Rent-A-Car Management System, a comprehensive application designed to streamline the management of car rentals. This project aims to provide an intuitive and efficient way to handle vehicle rentals, customer management, and booking operations.

## Overview

The Rent-A-Car Management System is a Python-based application that enables users to manage a car rental service. It offers functionalities for managing cars, customers, and bookings, ensuring a seamless and organized process for both the service providers and the customers.

## Features

- **Car Management**: Add, update, list, and remove cars from the system. Each car can be identified uniquely, and relevant details such as price per day, availability, and specifications are managed efficiently.
- **Customer Management**: Add, update, list, and remove customers. Each customer has a unique ID and associated information, ensuring accurate record-keeping.
- **Booking Management**: Manage bookings with ease. This includes creating new bookings, updating existing ones, listing all bookings, and removing bookings. The system ensures that cars are available for the specified dates and handles pricing calculations including discounts for extended rentals.
- **Date Validation**: Ensures that all dates entered follow the `YYYY-MM-DD` format and verifies that the end date is after the start date.
- **ID Management**: Generates unique IDs for cars, customers, and bookings, ensuring no conflicts and easy reference.
- **Data Persistence**: Utilizes JSON files to store data persistently, ensuring that all records are saved between sessions.

## Project Structure

```plaintext
rentacarproject/
├── data/
│   ├── listautomovel.json
│   ├── listbooking.json
│   └── listcliente.json
├── models/
│   ├── __init__.py
│   ├── automovel.py
│   ├── booking.py
│   └── cliente.py
├── services/
│   ├── __init__.py
│   ├── automovel_service.py
│   ├── booking_service.py
│   ├── cliente_service.py
│   └── pesquisas_service.py
├── utils/
│   ├── __init__.py
│   └── json_utils.py
├── main.py
└── README.md
```

## Installation

To run the Rent-A-Car Management System locally, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/rentacarproject.git
    cd rentacarproject
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the application:**
    ```sh
    python main.py
    ```

## Usage

The system presents a text-based menu interface where you can navigate through different options for managing cars, customers, and bookings. Simply follow the on-screen prompts to perform various actions. Here is a brief overview of the available commands:

- **Manage Cars**: Add new cars, update existing car details, list all cars, and remove cars.
- **Manage Customers**: Add new customers, update customer details, list all customers, and remove customers.
- **Manage Bookings**: Create new bookings, update bookings, list all bookings, and remove bookings. The system ensures date validation and checks for car availability.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

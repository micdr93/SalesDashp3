import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sales_leaderboardp3')


def welcome():
    print('Sales Dashboard')


class Person:
    def __init__(self, name, sales_target, revenue_to_date, new_deals, new_revenue):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date
        self.new_deals = new_deals
        self.new_revenue = new_revenue
        self.new_revenue_target = 10000

    def calculate_pacing(self):
        return self.revenue_to_date / self.sales_target

    def calculate_new_revenue_pacing(self):
        return self.new_revenue / self.new_revenue_target


class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def print_leaderboard(self):
        for person in self.persons:
            pacing = person.calculate_pacing()
            pacing_str = f"{pacing:.2%}"
            color_code = Fore.GREEN if pacing >= 1 else Fore.RED
            new_revenue_pacing = person.calculate_new_revenue_pacing()
            new_revenue_str = f"{new_revenue_pacing:.2%}"
            new_color = Fore.GREEN if new_revenue_pacing >= 1 else Fore.RED
            print(f"Name: {person.name}")
            print(f"Sales Target: {person.sales_target}")
            print(f"Revenue to Date: {person.revenue_to_date}")
            print(f"Pacing to Target: {color_code}{pacing_str}{Style.RESET_ALL}")
            print(f"New Product Deals: {person.new_deals}")
            print(f"New Product Revenue: {person.new_revenue}")
            print(f"New Revenue Pacing: {new_color}{new_revenue_str}{Style.RESET_ALL}")
            print("-" * 30)

    def search_person(self, name):
        for person in self.persons:
            if name.lower() in person.name.lower():
                return person
        return None

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)


def fetch_data_from_sheet(sheet):
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()[1:]
    persons = []
    for row in data:
        name, sales_target, revenue_to_date, new_deals, new_revenue = row
        sales_target = float(sales_target)
        revenue_to_date = float(revenue_to_date)
        new_deals = int(new_deals)
        new_revenue = float(new_revenue)
        person = Person(name, sales_target, revenue_to_date, new_deals, new_revenue)
        persons.append(person)
    return persons


def display_leaderboard():
    persons_from_sheet = fetch_data_from_sheet(SHEET)
    leaderboard = SalesLeaderboard(persons_from_sheet)
    leaderboard.rank_by_pacing()
    leaderboard.print_leaderboard()


def add_employee():
    name = get_name()
    sales_target = get_float_input("Enter sales target: ")
    revenue_to_date = get_float_input("Enter revenue to date: ")
    new_deals = get_int_input("Enter new product deals: ")
    new_revenue = get_float_input("Enter new product revenue: ")
    new_person = Person(name, sales_target, revenue_to_date, new_deals, new_revenue)

    SHEET.sheet1.append_row([
        new_person.name,
        new_person.sales_target,
        new_person.revenue_to_date,
        new_person.new_deals,
        new_person.new_revenue
    ])
    print("Employee added successfully.")


def get_name():
    while True:
        name = input("Enter employee name: ").strip()
        if name:
            return name
        print("Please enter a valid name")


def get_float_input(input_text):
    while True:
        try:
            value = float(input(input_text))
            if value >= 0:
                return value
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")


def get_int_input(input_text):
    while True:
        try:
            value = int(input(input_text))
            if value >= 0:
                return value
            else:
                print("Please enter a positive integer")
        except ValueError:
            print("Please enter a valid integer")


def main_menu():
    while True:
        print("\n1. Display Leaderboard")
        print("2. Add Employee")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_leaderboard()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-3.")


if __name__ == "__main__":
    welcome()
    main_menu()

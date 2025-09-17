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
    def __init__(self, name, sales_target, revenue_to_date, new_deals=0, new_revenue=0):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date
        self.new_deals = new_deals
        self.new_revenue = new_revenue

    def calculate_pacing(self):
        return self.revenue_to_date / self.sales_target if self.sales_target else 0

    def calculate_new_revenue_pacing(self):
        return self.new_revenue / 10000  # target 10,000 euros

class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def print_leaderboard(self):
        print(f"{'Name':<20} {'Sales Target':<15} {'Revenue':<15} {'Pacing':<10} "
              f"{'New Deals':<10} {'New Revenue':<15} {'Revenue Pacing':<15}")
        for person in self.persons:
            pacing = person.calculate_pacing()
            pacing_str = f"{pacing:.2%}"
            color_code = Fore.GREEN if pacing >= 1 else Fore.RED
            new_revenue_pacing = person.calculate_new_revenue_pacing()
            new_revenue_str = f"{new_revenue_pacing:.2%}"
            new_color = Fore.GREEN if new_revenue_pacing >= 1 else Fore.RED
            print(f"{person.name:<20} {person.sales_target:<15} {person.revenue_to_date:<15} "
                  f"{color_code}{pacing_str:<10}{Style.RESET_ALL} "
                  f"{person.new_deals:<10} {person.new_revenue:<15} {new_color}{new_revenue_str:<15}{Style.RESET_ALL}")

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)

def fetch_data_from_sheet(sheet):
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()[1:]
    persons = []
    for row in data:
        name = row[0]
        sales_target = float(row[1]) if len(row) > 1 and row[1] else 0
        revenue_to_date = float(row[2]) if len(row) > 2 and row[2] else 0
        new_deals = int(row[3]) if len(row) > 3 and row[3] else 0
        new_revenue = float(row[4]) if len(row) > 4 and row[4] else 0
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

    SHEET.sheet1.append_row([new_person.name, new_person.sales_target, new_person.revenue_to_date,
                             new_person.new_deals, new_person.new_revenue])
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
            value = input(input_text)
            value = float(value) if value else 0
            if value >= 0:
                return value
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")

def get_int_input(input_text):
    while True:
        try:
            value = input(input_text)
            value = int(value) if value else 0
            if value >= 0:
                return value
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")

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

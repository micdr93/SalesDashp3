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
        return self.new_revenue / 10000  # target 10,000 EUR

    def __str__(self):
        return f"{self.name:<15}{self.sales_target:<12}{self.revenue_to_date:<15}" \
               f"{self.new_deals:<12}{self.new_revenue:<15}"


class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def print_leaderboard(self):
        print(f"{'Name':<15}{'Target':<12}{'Revenue':<15}"
              f"{'Deals':<12}{'New Rev':<15}{'Pacing':<10}{'NP Pacing':<10}")
        for p in self.persons:
            pacing = f"{p.calculate_pacing():.0%}"
            np_pacing = f"{p.calculate_new_revenue_pacing():.0%}"
            pacing_color = Fore.GREEN if p.calculate_pacing() >= 1 else Fore.RED
            np_color = Fore.GREEN if p.calculate_new_revenue_pacing() >= 1 else Fore.RED
            print(f"{p.name:<15}{p.sales_target:<12}{p.revenue_to_date:<15}"
                  f"{p.new_deals:<12}{p.new_revenue:<15}"
                  f"{pacing_color}{pacing:<10}{np_color}{np_pacing:<10}{Style.RESET_ALL}")

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)


def fetch_data_from_sheet(sheet):
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()[1:]
    persons = []
    for row in data:
        while len(row) < 5:
            row.append('0')
        name, sales_target, revenue_to_date, new_deals, new_revenue = row
        sales_target = float(sales_target) if sales_target else 0
        revenue_to_date = float(revenue_to_date) if revenue_to_date else 0
        new_deals = int(new_deals) if new_deals else 0
        new_revenue = float(new_revenue) if new_revenue else 0
        person = Person(name, sales_target, revenue_to_date, new_deals, new_revenue)
        persons.append(person)
    return persons


def display_leaderboard():
    persons = fetch_data_from_sheet(SHEET)
    leaderboard = SalesLeaderboard(persons)
    leaderboard.rank_by_pacing()
    leaderboard.print_leaderboard()


def add_employee():
    name = input("Enter employee name: ").strip()
    sales_target = get_float_input("Enter sales target: ")
    revenue_to_date = get_float_input("Enter revenue to date: ")
    new_deals = get_int_input("Enter new product deals: ")
    new_revenue = get_float_input("Enter new product revenue: ")
    SHEET.sheet1.append_row([name, sales_target, revenue_to_date, new_deals, new_revenue])
    print("Employee added successfully.")


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            print("Enter a positive number")
        except ValueError:
            print("Invalid input")


def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Enter a positive integer")
        except ValueError:
            print("Invalid input")


def main_menu():
    while True:
        print("\n1. Display Leaderboard\n2. Add Employee\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            display_leaderboard()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    welcome()
    main_menu()

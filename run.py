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
    def __init__(self, name, sales_target, revenue_to_date, new_revenue):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date
        self.new_revenue = new_revenue

    def pacing(self):
        return self.revenue_to_date / self.sales_target if self.sales_target else 0

    def np_pacing(self):
        return self.new_revenue / 10000 if 10000 else 0


class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def print_leaderboard(self):
        print(f"{'Name':<12} {'Target':<12} {'Revenue':<12} {'New Product':<14}"
              f"{'Pacing':<10} {'NP Pacing':<10}")
        print("-" * 70)

        total_target = total_revenue = total_new = 0
        for p in self.persons:
            name_color = Fore.LIGHTBLUE_EX
            revenue_color = Fore.LIGHTBLUE_EX if p.revenue_to_date < p.sales_target else Fore.GREEN
            pace_color = Fore.GREEN if p.pacing() >= 1 else Fore.RED
            np_color = Fore.GREEN if p.np_pacing() >= 1 else Fore.RED
            print(f"{name_color}{p.name:<12}{Style.RESET_ALL}"
                  f"€{p.sales_target:<11,.0f}"
                  f"{revenue_color}€{p.revenue_to_date:<11,.0f}{Style.RESET_ALL}"
                  f"€{p.new_revenue:<11,.0f}"
                  f"{pace_color}{p.pacing():<9.0%}{Style.RESET_ALL}"
                  f"{np_color}{p.np_pacing():<9.0%}{Style.RESET_ALL}")

            total_target += p.sales_target
            total_revenue += p.revenue_to_date
            total_new += p.new_revenue

        overall_pacing = total_revenue / total_target if total_target else 0
        overall_np_pacing = total_new / (len(self.persons) * 10000) if self.persons else 0

        print("-" * 70)
        print(f"{'Overall':<12} €{total_target:<11,.0f} €{total_revenue:<11,.0f} €{total_new:<11,.0f}"
              f"{Fore.GREEN if overall_pacing >= 1 else Fore.RED}{overall_pacing:<9.0%}{Style.RESET_ALL}"
              f"{Fore.GREEN if overall_np_pacing >= 1 else Fore.RED}{overall_np_pacing:<9.0%}{Style.RESET_ALL}")

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.pacing(), reverse=True)


def fetch_data_from_sheet(sheet):
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()[1:]
    persons = []
    for row in data:
        name, sales_target, revenue_to_date, new_revenue = row
        sales_target = float(sales_target) if sales_target else 0
        revenue_to_date = float(revenue_to_date) if revenue_to_date else 0
        new_revenue = float(new_revenue) if new_revenue else 0
        persons.append(Person(name, sales_target, revenue_to_date, new_revenue))
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
    new_revenue = get_float_input("Enter new product revenue: ")
    new_person = Person(name, sales_target, revenue_to_date, new_revenue)
    SHEET.sheet1.append_row([new_person.name, new_person.sales_target, new_person.revenue_to_date, new_person.new_revenue])
    print("Employee added successfully.")


def get_name():
    while True:
        name = input("Enter employee name: ").strip()
        if name:
            return name
        print("Please enter a valid name")


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("Enter a positive number")
        except ValueError:
            print("Enter a valid number")


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
            print("Invalid choice. Enter 1-3.")


if __name__ == "__main__":
    welcome()
    main_menu()

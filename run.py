import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Style

SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sales_leaderboardp3')


def welcome():
    print('Sales Dashboard')


class Person:
    def __init__(self, name, sales_target, revenue_to_date, new_revenue=0):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date
        self.new_revenue = new_revenue

    def pacing(self):
        return self.revenue_to_date / self.sales_target if self.sales_target else 0

    def np_pacing(self):
        return self.new_revenue / 10000

    def __str__(self):
        return f"{self.name:<10}{self.sales_target:<10}{self.revenue_to_date:<10}{self.new_revenue:<10}"


class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def rank(self):
        self.persons.sort(key=lambda x: x.pacing(), reverse=True)

    def team_summary(self):
        total_target = sum(p.sales_target for p in self.persons)
        total_revenue = sum(p.revenue_to_date for p in self.persons)
        total_new = sum(p.new_revenue for p in self.persons)
        team_size = len(self.persons)
        overall_pacing = total_revenue / total_target if total_target else 0
        overall_np = total_new / (team_size * 10000) if team_size else 0
        op_color = Fore.GREEN if overall_pacing >= 1 else Fore.RED
        np_color = Fore.GREEN if overall_np >= 1 else Fore.RED
        print(f"Team: Target={total_target} Rev={total_revenue} NewRev={total_new}")
        print(f"Pacing: {op_color}{overall_pacing:.0%}{Style.RESET_ALL} "
              f"| NP Pacing: {np_color}{overall_np:.0%}{Style.RESET_ALL}\n")

    def print_leaderboard(self):
        self.team_summary()
        print("Name      Target    Rev       NewRev   Pace   NPace")
        for p in self.persons:
            name_color = Fore.LIGHTBLUE_EX
            revenue_color = Fore.LIGHTBLUE_EX
            pace_color = Fore.GREEN if p.pacing() >= 1 else Fore.RED
            np_color = Fore.GREEN if p.np_pacing() >= 1 else Fore.RED
            print(f"{name_color}{p.name:<10}{Style.RESET_ALL}"
                  f"{p.sales_target:<10}"
                  f"{revenue_color}{p.revenue_to_date:<10}{Style.RESET_ALL}"
                  f"{p.new_revenue:<10}"
                  f"{pace_color}{p.pacing():.0%}{Style.RESET_ALL}   "
                  f"{np_color}{p.np_pacing():.0%}{Style.RESET_ALL}")


def fetch_data(sheet):
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()[1:]
    persons = []
    for row in data:
        while len(row) < 4:
            row.append('0')
        name, target, revenue, new_rev = row
        persons.append(Person(name, float(target or 0), float(revenue or 0), float(new_rev or 0)))
    return persons


def display_leaderboard():
    lb = SalesLeaderboard(fetch_data(SHEET))
    lb.rank()
    lb.print_leaderboard()


def add_employee():
    name = input("Name: ").strip()
    target = get_float("Sales Target: ")
    revenue = get_float("Revenue: ")
    new_rev = get_float("New Product Rev: ")
    SHEET.sheet1.append_row([name, target, revenue, new_rev])
    print("Employee added!")


def get_float(prompt):
    while True:
        try:
            val = float(input(prompt))
            if val >= 0:
                return val
            print("Enter a positive number")
        except ValueError:
            print("Invalid input")


def main_menu():
    while True:
        print("\n1.Display 2.Add 3.Exit")
        choice = input("Choice: ")
        if choice == "1":
            display_leaderboard()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            break
        else:
            print("Invalid")


if __name__ == "__main__":
    welcome()
    main_menu()

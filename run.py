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


class Person:
    def __init__(self, name, sales_target, revenue_to_date, new_revenue):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date
        self.new_revenue = new_revenue

    def pacing(self):
        return self.revenue_to_date / self.sales_target if self.sales_target else 0

    def np_pacing(self):
        return self.new_revenue / 10000  # target 10,000€ for new product revenue


class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.pacing(), reverse=True)

    def print_leaderboard(self):
        print(f"{'Name':<12}{'Target':<10}{'Revenue':<10}{'New Product':<12}"
              f"{'Pacing':<8}{'NP Pacing':<10}")
        total_target = total_revenue = total_new = 0
        for p in self.persons:
            name_color = Fore.LIGHTBLUE_EX
            revenue_color = Fore.LIGHTBLUE_EX if p.revenue_to_date < p.sales_target else Fore.GREEN
            pace_color = Fore.GREEN if p.pacing() >= 1 else Fore.RED
            np_color = Fore.GREEN if p.np_pacing() >= 1 else Fore.RED
            print(f"{name_color}{p.name:<12}{Style.RESET_ALL}"
                  f"€{p.sales_target:<9,.0f}"
                  f"{revenue_color}€{p.revenue_to_date:<9,.0f}{Style.RESET_ALL}"
                  f"€{p.new_revenue:<9,.0f}"
                  f"{pace_color}{p.pacing():.0%}{Style.RESET_ALL}   "
                  f"{np_color}{p.np_pacing():.0%}{Style.RESET_ALL}")
            total_target += p.sales_target
            total_revenue += p.revenue_to_date
            total_new += p.new_revenue
        overall_pacing = total_revenue / total_target if total_target else 0
        overall_np_pacing = total_new / (len(self.persons) * 10000) if self.persons else 0
        print(f"\n{'Overall':<12}€{total_target:<9,.0f}€{total_revenue:<9,.0f}€{total_new:<9,.0f}"
              f"{Fore.GREEN if overall_pacing >= 1 else Fore.RED}{overall_pacing:.0%}{Style.RESET_ALL}   "
              f"{Fore.GREEN if overall_np_pacing >= 1 else Fore.RED}{overall_np_pacing:.0%}{Style.RESET_ALL}")


def fetch_data_from_sheet(sheet):
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()[1:]
    persons = []
    for row in data:
        if len(row) < 4: continue
        name, target, revenue, new_rev = row
        try:
            persons.append(Person(name, float(target), float(revenue), float(new_rev)))
        except:
            continue
    return persons


def display_leaderboard():
    persons = fetch_data_from_sheet(SHEET)
    leaderboard = SalesLeaderboard(persons)
    leaderboard.rank_by_pacing()
    leaderboard.print_leaderboard()


def add_employee():
    name = input("Enter employee name: ").strip()
    sales_target = float(input("Enter sales target: "))
    revenue_to_date = float(input("Enter revenue to date: "))
    new_revenue = float(input("Enter new product revenue: "))
    SHEET.sheet1.append_row([name, sales_target, revenue_to_date, new_revenue])
    print("Employee added successfully.")


def main_menu():
    print("Sales Dashboard")
    while True:
        print("\n1. Display Leaderboard\n2. Add Employee\n3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            display_leaderboard()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main_menu()

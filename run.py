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
    def __init__(self, name, sales_target, revenue_to_date):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date

    def calculate_pacing(self):
        return self.revenue_to_date / self.sales_target

    def __str__(self):
        return f"{self.name:<20} {self.sales_target:<15} {self.revenue_to_date:<20}"

class SalesLeaderboard:
    def __init__(self, persons):
        self.persons = persons

    def print_leaderboard(self):
        print(f"{'Name':<20} {'Sales Target':<15} {'Revenue to Date':<20} {'Pacing to Target':<20}")
        for person in self.persons:
            pacing = person.calculate_pacing()
            pacing_str = f"{pacing:.2%}"
            if pacing >= 1:
                pacing_str = Fore.GREEN + pacing_str + Style.RESET_ALL
            else:
                pacing_str = Fore.RED + pacing_str + Style.RESET_ALL
            print(f"{person.name:<20} {person.sales_target:<15} {person.revenue_to_date:<20} {pacing_str:<20}")

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
        name, sales_target, revenue_to_date = row
        sales_target = float(sales_target)
        revenue_to_date = float(revenue_to_date)
        person = Person(name, sales_target, revenue_to_date)
        persons.append(person)
    return persons

def display_leaderboard():
    persons_from_sheet = fetch_data_from_sheet(SHEET)
    leaderboard = SalesLeaderboard(persons_from_sheet)
    leaderboard.rank_by_pacing()
    leaderboard.print_leaderboard()

def add_employee():
    name = input("Enter employee name: ")
    sales_target = float(input("Enter sales target: "))
    revenue_to_date = float(input("Enter revenue to date: "))
    new_person = Person(name, sales_target, revenue_to_date)
    # Append the new person to the Google Sheet
    SHEET.sheet1.append_row([new_person.name, new_person.sales_target, new_person.revenue_to_date])
    print("Employee added successfully.")

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
    main_menu()

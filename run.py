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
SHEET = GSPREAD_CLIENT.open('Sales_DashboardP3')

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
            pacing_str = (Fore.GREEN if pacing >= 1 else Fore.RED) + pacing_str + Style.RESET_ALL
            print(f"{person} {pacing_str:<20}")

    def search_person(self, name):
        for person in self.persons:
            if name.lower() in person.name.lower():
                return person
        return None

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)

def main_menu():
    persons = []

    while True:
        print("\n1. Add Person")
        print("2. Edit Person")
        print("3. List Persons")
        print("4. View Sales Leaderboard")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_person(persons)
        elif choice == "2":
            edit_person(persons)
        elif choice == "3":
            list_persons(persons)
        elif choice == "4":
            view_sales_leaderboard(persons)
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")

def add_person(persons):
    name = input("Enter person's name: ")
    sales_target = float(input("Enter sales target: "))
    revenue_to_date = float(input("Enter revenue to date: "))
    person = Person(name, sales_target, revenue_to_date)
    persons.append(person)
    print("Person added successfully.")

def edit_person(persons):
    name = input("Enter the name of the person to edit: ")
    for person in persons:
        if person.name.lower() == name.lower():
            new_sales_target = float(input(f"Enter new sales target for {name}: "))
            new_revenue_to_date = float(input(f"Enter new revenue to date for {name}: "))
            person.sales_target = new_sales_target
            person.revenue_to_date = new_revenue_to_date
            print("Person updated successfully.")
            return
    print("Person not found.")

def list_persons(persons):
    for person in persons:
        print(person)

        

def view_sales_leaderboard(persons):
    leaderboard = SalesLeaderboard(persons)
    leaderboard.rank_by_pacing()
    leaderboard.print_leaderboard()

    search_name = input("\nEnter the name of the person you want to search for: ")
    person = leaderboard.search_person(search_name)
    if person:
        print("\nPerson found:")
        print(f"Name: {person.name}")
        print(f"Sales Target: {person.sales_target}")
        print(f"Revenue to Date: {person.revenue_to_date}")
    else:
        print("\nPerson not found.")

if __name__ == "__main__":
    main_menu()

import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Authorize the Google Sheets API
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
            if pacing >= 1:
                pacing_str = Fore.GREEN + pacing_str + Style.RESET_ALL
            else:
                pacing_str = Fore.RED + pacing_str + Style.RESET_ALL
            print(f"{person} {pacing_str:<20}")

    def search_person(self, name):
        for person in self.persons:
            if name.lower() in person.name.lower():
                return person
        return None

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)

# Define the sales data with Person class
sales_data = [
    Person("Liam O'Connor", 100000, 78500),
    Person("Aoife Murphy", 75000, 63200),
    Person("Sean Kelly", 120000, 95800),
    Person("Ciara Ryan", 90000, 71300),
    Person("Conor Byrne", 110000, 88600),
    Person("Saoirse Doyle", 80000, 67500),
    Person("Cian O'Sullivan", 95000, 79400),
    Person("Niamh Walsh", 85000, 85600),
    Person("Eoin McCarthy", 70000, 58200),
    Person("Aoibhinn Kennedy", 105000, 84700),
    Person("Finnegan Hughes", 115000, 91600),
    Person("Sinead O'Donnell", 65000, 53800),
    Person("Padraig Fitzgerald", 125000, 99200),
    Person("Aisling Brennan", 82000, 68900),
    Person("Oisin Flynn", 88000, 74600),
    Person("Roisin Gallagher", 97000, 81300),
    Person("Declan O'Rourke", 72000, 59800),
    Person("Eimear Clarke", 78000, 65400),
    Person("Colm Ryan", 93000, 77900),
    Person("Grainne O'Neill", 87000, 73100)
]

# Assuming we'll store persons in a list
persons = []

def add_person():
    name = input("Enter person's name: ")
    sales_target = float(input("Enter sales target: "))
    revenue_to_date = float(input("Enter revenue to date: "))
    person = Person(name, sales_target, revenue_to_date)
    persons.append(person)
    print("Person added successfully.")

def edit_person():
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

def main_menu():
    while True:
        print("\n1. Add Person")
        print("2. Edit Person")
        print("3. List Persons")
        print("4. View Sales Leaderboard")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_person()
        elif choice == "2":
            edit_person()
        elif choice == "3":
            for person in persons:
                print(person)
        elif choice == "4":
            # Create the leaderboard
            leaderboard = SalesLeaderboard(persons + sales_data)  # Add sales_data to the existing persons

            # Rank persons by pacing
            leaderboard.rank_by_pacing()

            # Print the leaderboard
            leaderboard.print_leaderboard()

            # Example usage of the search function
            search_name = input("\nEnter the name of the person you want to search for: ")
            person = leaderboard.search_person(search_name)
            if person:
                print("\nPerson found:")
                print(f"Name: {person.name}")
                print(f"Sales Target: {person.sales_target}")
                print(f"Revenue to Date: {person.revenue_to_date}")
            else:
                print("\nPerson not found.")
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main_menu()

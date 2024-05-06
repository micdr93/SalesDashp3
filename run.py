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

class SalesEmployee:
    def __init__(self, name, sales_target, revenue_to_date):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date

    def calculate_pacing(self):
        return self.revenue_to_date / self.sales_target

    def __str__(self):
        return f"{self.name:<20} {self.sales_target:<15} {self.revenue_to_date:<20}"

class SalesLeaderboard:
    def __init__(self, employees):
        self.employees = employees

    def print_leaderboard(self):
        print(f"{'Name':<20} {'Sales Target':<15} {'Revenue to Date':<20} {'Pacing to Target':<20}")
        for employee in self.employees:
            pacing = employee.calculate_pacing()
            pacing_str = f"{pacing:.2%}"
            if pacing >= 1:
                pacing_str = Fore.GREEN + pacing_str + Style.RESET_ALL
            else:
                pacing_str = Fore.RED + pacing_str + Style.RESET_ALL
            print(f"{employee} {pacing_str:<20}")

    def search_employee(self, name):
        for employee in self.employees:
            if name.lower() in employee.name.lower():
                return employee
        return None

    def rank_by_pacing(self):
        self.employees.sort(key=lambda x: x.calculate_pacing(), reverse=True)

# Define the sales data
sales_data = [
    SalesEmployee("Liam O'Connor", 100000, 78500),
    SalesEmployee("Aoife Murphy", 75000, 63200),
    SalesEmployee("Sean Kelly", 120000, 95800),
    SalesEmployee("Ciara Ryan", 90000, 71300),
    SalesEmployee("Conor Byrne", 110000, 88600),
    SalesEmployee("Saoirse Doyle", 80000, 67500),
    SalesEmployee("Cian O'Sullivan", 95000, 79400),
    SalesEmployee("Niamh Walsh", 85000, 85600),
    SalesEmployee("Eoin McCarthy", 70000, 58200),
    SalesEmployee("Aoibhinn Kennedy", 105000, 84700),
    SalesEmployee("Finnegan Hughes", 115000, 91600),
    SalesEmployee("Sinead O'Donnell", 65000, 53800),
    SalesEmployee("Padraig Fitzgerald", 125000, 99200),
    SalesEmployee("Aisling Brennan", 82000, 68900),
    SalesEmployee("Oisin Flynn", 88000, 74600),
    SalesEmployee("Roisin Gallagher", 97000, 81300),
    SalesEmployee("Declan O'Rourke", 72000, 59800),
    SalesEmployee("Eimear Clarke", 78000, 65400),
    SalesEmployee("Colm Ryan", 93000, 77900),
    SalesEmployee("Grainne O'Neill", 87000, 73100)
]
# Create the leaderboard
leaderboard = SalesLeaderboard(sales_data)

# Rank employees by pacing
leaderboard.rank_by_pacing()

# Print the leaderboard
leaderboard.print_leaderboard()

# Example usage of the search function
search_name = input("\nEnter the name of the employee you want to search for: ")
employee = leaderboard.search_employee(search_name)
if employee:
    print("\nEmployee found:")
    print(f"Name: {employee.name}")
    print(f"Sales Target: {employee.sales_target}")
    print(f"Revenue to Date: {employee.revenue_to_date}")
else:
    print("\nEmployee not found.")
    
class Person:
    def __init__(self, first_name, last_name, attribute1, attribute2):
        self.first_name = first_name
        self.last_name = last_name
        self.attribute1 = attribute1
        self.attribute2 = attribute2

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Attribute 1: {self.attribute1}, Attribute 2: {self.attribute2}"

# Assuming we'll store persons in a list
persons = []

def add_person():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    attribute1 = input("Enter Attribute 1: ")
    attribute2 = input("Enter Attribute 2: ")
    person = Person(first_name, last_name, attribute1, attribute2)
    persons.append(person)
    print("Person added successfully.")

def edit_person():
    first_name = input("Enter the first name of the person to edit: ")
    last_name = input("Enter the last name of the person to edit: ")
    for person in persons:
        if person.first_name == first_name and person.last_name == last_name:
            new_attribute1 = input(f"Enter new Attribute 1 for {first_name} {last_name}: ")
            new_attribute2 = input(f"Enter new Attribute 2 for {first_name} {last_name}: ")
            person.attribute1 = new_attribute1
            person.attribute2 = new_attribute2
            print("Person updated successfully.")
            return
    print("Person not found.")

def main_menu():
    while True:
        print("\n1. Add Person")
        print("2. Edit Person")
        print("3. List Persons")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_person()
        elif choice == "2":
            edit_person()
        elif choice == "3":
            for person in persons:
                print(person)
        elif choice == "4":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-4.")

if __name__ == "__main__":
    main_menu()
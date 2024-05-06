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

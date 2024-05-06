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
            print(f"{person} {pacing_str:<20}")

    def search_person(self, name):
        for person in self.persons:
            if name.lower() in person.name.lower():
                return person
        return None

    def rank_by_pacing(self):
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)

def fetch_data_from_sheet(sheet):
    data = sheet.get_all_values()[1:]  # Exclude header row
    persons = []
    for row in data:
        name, sales_target, revenue_to_date = row
        sales_target = float(sales_target)
        revenue_to_date = float(revenue_to_date)
        person = Person(name, sales_target, revenue_to_date)
        persons.append(person)
    return persons

def main():
   
    persons_from_sheet = fetch_data_from_sheet(SHEET)

    leaderboard = SalesLeaderboard()

    
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
    main()

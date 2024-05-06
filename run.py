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
    """
    Represents a person with sales-related attributes.

    Args:
        name (str): The name of the person.
        sales_target (float): The sales target of the person.
        revenue_to_date (float): The revenue generated by the person to date.
    """

    def __init__(self, name, sales_target, revenue_to_date):
        self.name = name
        self.sales_target = sales_target
        self.revenue_to_date = revenue_to_date

    def calculate_pacing(self):
        """Calculate the pacing of revenue to sales target."""
        return self.revenue_to_date / self.sales_target

    def __str__(self):
        """String representation of the Person object."""
        return
        f"{self.name:<20}"
        f"{self.sales_target:<15} {self.revenue_to_date:<20}"


class SalesLeaderboard:
    """
    Represents a sales leaderboard.

    Args:
        persons (list): List of Person objects representing salespersons.
    """

    def __init__(self, persons):
        self.persons = persons

    def print_leaderboard(self):
        """Print the sales leaderboard."""
        print(
            f"{'Name':<20} {'Sales Target':<15}"
            f"{'Revenue to Date':<20} {'Pacing to Target':<20}")
        for person in self.persons:
            pacing = person.calculate_pacing()
            pacing_str = f"{pacing:.2%}"
            color_code = self.get_color_code(pacing)
            print(
                f"{person.name:<20} {person.sales_target:<15} "
                f"{person.revenue_to_date:<20} "
                f"{color_code}{pacing_str:<20}{Style.RESET_ALL}")

    def search_person(self, name):
        """
        Search for a person by name.

        Args:
            name (str): The name to search for.

        Returns:
            Person or None: The Person object if found, otherwise None.
        """
        for person in self.persons:
            if name.lower() in person.name.lower():
                return person
        return None

    def rank_by_pacing(self):
        """Sort persons by pacing to target."""
        self.persons.sort(key=lambda x: x.calculate_pacing(), reverse=True)

    @staticmethod
    def get_color_code(pacing):
        """
        Get color code based on the pacing.

        Args:
            pacing (float): The pacing value.

        Returns:
            str: Color code for colorama.
        """
        if pacing >= 1:
            return Fore.GREEN
        else:
            return Fore.RED


def fetch_data_from_sheet(sheet):
    """
    Fetch sales data from a Google Sheets document.

    Args:
        sheet: The Google Sheets document.

    Returns:
        list: List of Person objects representing salespersons.
    """
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
    """Display the sales leaderboard."""
    persons_from_sheet = fetch_data_from_sheet(SHEET)
    leaderboard = SalesLeaderboard(persons_from_sheet)
    leaderboard.rank_by_pacing()
    leaderboard.print_leaderboard()


def add_employee():
    """Add a new employee to the sales data."""
    name = get_name
    sales_target = get_float_input("Enter sales target: ")
    revenue_to_date = get_float_input("Enter revenue to date: ")
    new_person = Person(name, sales_target, revenue_to_date)
    # Append the new person to the Google Sheet
    SHEET.sheet1.append_row(
        [new_person.name, new_person.sales_target, new_person.revenue_to_date]
    )
    print("Employee added successfully.")

def get_name():
    while True:
        name = input("Enter employee name: ").strip()
        if name:
            return name
        print("Please enter a valid name")

def get_float_input(input_text):
    while True:
        try:
            value = float(input(input_text))
            if value >= 0:
                return value
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")

def main_menu():
    """Display the main menu and handle user inputs."""
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

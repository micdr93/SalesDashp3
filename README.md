# Sales Dashboard 

The Sales Dashboard provides a convenient interface for users to monitor the current sales performance of salespeople. Additionally, it offers functionality to add new employees along with their respective sales targets and current sales figures.

![Run Program](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/run.png)


|  | User Stories                                   | Description                                          |
|----------|------------------------------------------------|------------------------------------------------------|
| 1        | As a user, I want to view sales performance   | Users can monitor the current sales performance of salespeople |
| 2        | As a user, I want to add new employees         | Users can add new employees|
| 3        | As a user, I want to assign a sales target to a new employee | Users can assign a sales target to a new employee |
| 4        | As a user, I want to add current sales figures to the new employees | Users can add a current sales figure to the salesperson |

## Data Models 
- The Sales Dashboard's data model encompasses entities such as Employees, Sales, and Targets. 
- Within this model, each Employee record comprises essential details like name, ID, and assigned sales target. 
- Sales records encapsulate specific sale information, including the transaction amount and date. 
- Targets records maintain the predefined sales objectives for individual employees.


## Flowchart

- I made the flowchart made with [Lucid Chart](https://lucidchart.com/) to map it out:
![flowchart](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/Flowchart%20(1).png)

## Features: 

- View current sales performance of salespeople.
- Add new employees with sales targets and current sales figures.
- It uses the library colorama to give an indication of top performers.
- It uses Google Sheets to store the data.

Running the program prompts you to select between 3 options:

![run](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/run.png)

Option 1 displays the leaderboard to the user

- Display Leaderboard
![display leaderboard](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/display_leaderboard.png)

Option 2 allows the user to enter an employee name.

- Enter Employee Name
![enter employee name](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/enter_employee_name.png)

From that point on you can assign the salesperson a sales target.

- Enter Employee Sales Target
![enter sales target](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/enter_sales_target.png)

After that you can add the current sales figures for that employee.

- Enter Employee Revenue to Date
![Enter Employee Revenue to Date](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/enter_rev_to_date.png)

The employee has now been added successfully.

- Employee Added Succcessfully
![Employee Added Succcessfully](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/employee_added_successfully.png)

- Google Sheets
![Google Sheets](https://github.com/micdr93/SalesDashp3/blob/main/assets/readme_files/google_sheets_setup.png)

### Languages, Frameworks, Libraries Used:

- [Python](https://www.python.org/)

- [GitPod](https://gitpod.io/) was used for writing, editing, committing and pushing to Github.

- [GitHub](https://github.com/)

- [Colorama](https://pypi.org/project/colorama/) was used to indicate the top sales performers. 

 - [CI Python Linter](https://pep8ci.herokuapp.com/#) was used to validate the code.

 - [Heroku](https://id.heroku.com) the application was deployed on Heroku.










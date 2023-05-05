
# Financial Calculator

This project is a web application for a financial calculator that helps users plan their retirement by providing various investment strategies based on their current age, desired retirement age, current savings, annual contributions, and desired net worth at retirement.

## Introduction

The financial calculator allows users to input their financial data and provides a set of recommendations for Conservative, Moderate, and Aggressive investment strategies. This helps users make informed decisions about their investments to achieve their desired retirement goals.

## Technical Architecture

The application is built using Flask, a Python-based micro-framework. It utilizes:

1. Flask-SQLAlchemy for database management.
2. Flask-Migrate for database migration.
3. Flask-Login for user authentication and session management.
4. Flask-Session for server-side session storage.

The application follows the MVC (Model-View-Controller) design pattern. The `User` and `CalculationResult` models handle the database schema and relationships. The `app.py` file contains the views and routes for handling user registration, login, calculator, and results pages.

## Installation Instructions

To set up the project locally, follow these steps:

1. Clone the repository to your local machine.

   ```
   git clone https://github.com/hammadali224/cs222-web-project.git
   cd cs222-web-project
   ```

2. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages using the `requirements.txt` file:

   ```
   pip install -r requirements.txt
   ```

4. Run the database migration to set up the database:

   ```
   python3 -m flask db init
   python3 -m flask db migrate
   python3 -m flask db upgrade
   ```

5. Run the application:

   ```
   python3 app.py
   ```

6. Access the application in your browser at `http://localhost:5000`.

## Usage

1. Open the application in your web browser.
2. Register a new user account or log in with an existing account.
3. Enter your financial information and desired retirement age in the calculator form.
4. Click "Calculate" to view your projected retirement savings for different investment strategies.

## Technologies Used

- Flask web framework
- Flask-SQLAlchemy for database management
- Flask-Migrate for database migrations
- Flask-Login for user authentication
- SQLite as the database

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

Feel free to modify, distribute, or use this project as you see fit, provided you include the copyright notice and the permission notice in all copies or substantial portions of the software.

## Group Members and Roles

1. Siddhesh Agarwal - Backend development, database management, and Flask integration.

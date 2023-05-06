# cs222-web-project

Project name: Financial Calculator

Our project defines a Flask web application that allows users to input financial information and calculates if they are on track to retire with their desired income.

The calculate() function in app.py takes in multiple arguments that represent the user's financial information, including their yearly salary, current age, desired retirement age, desired annual income during retirement, annual interest rate, present savings, periodic payment, starting principal, annual contribution, and inflation rate.

It first checks that all input values are valid numbers and positive. Then, it calculates the number of years until retirement and the future value of the user's current savings, periodic payments, and annual contributions. It also adjusts the desired annual income during retirement for inflation. Finally, it calculates the amount the user needs to save each year to reach their retirement savings goal and determines if the user is on track to retire with their desired income.

The index() function handles the GET and POST requests to the application. If the request is a POST request, it retrieves the user's input values, passes them to the calculate() function to calculate the result, and renders the result on the HTML template. If the request is a GET request, it simply renders the HTML template with no result.

Overall, this code provides a basic framework for a retirement calculator web application. However, it could be improved by including error messages for invalid input values and improving the user interface.

Roles and Responsibilites 

Hammad Ali : Front-end development

Fawzan Ali : Integration and App development

Siddhesh Agarwal : Back-end development and Database management

Vijwal Rao Akula : Algorithm Development and Testing


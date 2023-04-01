from flask import Flask, request, render_template

app = Flask(__name__)

def calculate(yearly_salary, current_age, desired_retirement_age, 
              desired_annual_income_during_retirement, annual_interest_rate, 
              present_savings, periodic_payment, starting_principal, 
              annual_contribution, inflation_rate):

    # Check that all input values are valid numbers
    try:
        yearly_salary = float(yearly_salary)
        current_age = int(current_age)
        desired_retirement_age = int(desired_retirement_age)
        desired_annual_income_during_retirement = float(desired_annual_income_during_retirement)
        annual_interest_rate = float(annual_interest_rate)
        present_savings = float(present_savings)
        periodic_payment = float(periodic_payment)
        starting_principal = float(starting_principal)
        annual_contribution = float(annual_contribution)
        inflation_rate = float(inflation_rate)
    except ValueError:
        return "Error: Please enter valid input values."

    # Check that all input values are positive
    if yearly_salary <= 0 or current_age <= 0 or desired_retirement_age <= 0 \
        or desired_annual_income_during_retirement <= 0 or annual_interest_rate <= 0 \
        or present_savings < 0 or periodic_payment < 0 or starting_principal < 0 \
        or annual_contribution < 0 or inflation_rate < 0:
        return "Error: Please enter positive input values."

    # Calculate the number of years until retirement
    years_until_retirement = desired_retirement_age - current_age

    # Calculate the future value of the user's current savings, periodic payments, and annual contributions
    future_value_current_savings = present_savings * (1 + annual_interest_rate/100) ** years_until_retirement
    future_value_periodic_payment = periodic_payment * ((1 + annual_interest_rate/100) ** years_until_retirement - 1) / (annual_interest_rate/100)
    future_value_annual_contribution = annual_contribution * (((1 + annual_interest_rate/100) ** years_until_retirement - 1) / (annual_interest_rate/100))

    # Calculate the total future value of the user's retirement savings
    future_value_total = future_value_current_savings + future_value_periodic_payment + future_value_annual_contribution

    # Adjust the desired annual income during retirement for inflation
    desired_annual_income_during_retirement_inflated = desired_annual_income_during_retirement * ((1 + inflation_rate/100) ** years_until_retirement)

    # Calculate the amount the user needs to save each year to reach their retirement savings goal
    yearly_savings_needed = (future_value_total - starting_principal) / (((1 + annual_interest_rate/100) ** years_until_retirement - 1) / (annual_interest_rate/100))

    # Check if the user is on track to retire at their desired retirement age and receive their desired annual income during retirement
    if yearly_savings_needed <= yearly_salary:
        result = f"You are on track to retire at age {desired_retirement_age} and receive your desired annual income of ${desired_annual_income_during_retirement:.2f} during retirement."
    else:
        result = f"You are not on track to retire at age {desired_retirement_age} and receive your desired annual income of ${desired_annual_income_during_retirement:.2f} during retirement. You need to save at least ${yearly_savings_needed:.2f} per year."
    
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the values entered by the user
        yearly_salary = request.form['idTxtInput1']
        current_age = request.form['idTxtInput2']
        desired_retirement_age = request.form['idTxtInput3']
        desired_annual_income_during_retirement = request.form['idTxtInput4']
        annual_interest_rate = request.form['idTxtInput5']
        present_savings = request.form['idTxtInput6']
        periodic_payment = request.form['idTxtInput7']
        starting_principal = request.form['idTxtInput8']
        annual_contribution = request.form['idTxtInput9']
        inflation_rate = request.form['idTxtInput10']

        # Calculate the result using the user's input values
        result = calculate(yearly_salary, current_age, desired_retirement_age, desired_annual_income_during_retirement, annual_interest_rate, present_savings, periodic_payment, starting_principal, annual_contribution, inflation_rate)

        # Render the result on the HTML template
        return render_template('index.html', result=result)
    else:
        # Render the HTML template with no result
        return render_template('index.html')

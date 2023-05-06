import os
import json 
from flask_login import current_user
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_calculator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    form_data = db.Column(db.String, nullable=True)

class CalculationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('calculation_results', lazy=True))
    conservative_savings = db.Column(db.Float, nullable=False)
    moderate_savings = db.Column(db.Float, nullable=False)
    aggressive_savings = db.Column(db.Float, nullable=False)
    recommendations = db.Column(db.String(255), nullable=False)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        try:
            session['form_data'] = request.form.to_dict()

            current_age = int(request.form['current_age'])
            desired_age = int(request.form['desired_age'])
            current_savings = float(request.form['current_savings'])
            annual_contributions = float(request.form['annual_contributions'])
            desired_net_worth = float(request.form['desired_net_worth'])


            investment_strategies = {
            'Conservative': 0.04,
            'Moderate': 0.06,
            'Aggressive': 0.08
            }

            years_to_retirement = desired_age - current_age
            savings = {}
            for strategy, rate in investment_strategies.items():
                future_value = current_savings * (1 + rate) ** years_to_retirement + \
                            annual_contributions * ((1 + rate) ** years_to_retirement - 1) / rate
                savings[strategy] = future_value

            recommendations = f"To achieve a net worth of ${desired_net_worth} by retirement, "
            if savings['Aggressive'] >= desired_net_worth:
                recommendations += "you should choose the Aggressive strategy."
            elif savings['Moderate'] >= desired_net_worth:
                recommendations += "you can choose either the Moderate or Aggressive strategy."
            elif savings['Conservative'] >= desired_net_worth:
                recommendations += "you can follow any of the three investment strategies."
            else:
                required_rate = (desired_net_worth - current_savings) / (annual_contributions * years_to_retirement)
                recommendations += f"you need to increase your annual contributions or aim for an annual return higher than {required_rate * 100:.2f}%."

            # Save the calculation results for the current user
            calculation_result = CalculationResult(user_id=current_user.id,
                                                   conservative_savings=savings['Conservative'],
                                                   moderate_savings=savings['Moderate'],
                                                   aggressive_savings=savings['Aggressive'],
                                                   recommendations=recommendations)
            db.session.add(calculation_result)
            db.session.commit()
            current_user.form_data = json.dumps(request.form.to_dict())
            db.session.commit()
            print(f"Saving form data for user {current_user.id}: {current_user.form_data}")  # Add this line

            return render_template('results.html',
                                   conservative_savings=savings['Conservative'],
                                   moderate_savings=savings['Moderate'],
                                   aggressive_savings=savings['Aggressive'],
                                   recommendations=recommendations)
        except ValueError:
            flash("Please enter valid numbers for all fields.", "error")
        except Exception as e:
            flash(f"An error occurred during the calculation: {str(e)}", "error")

        return render_template('FinancialCalculator.html', form_data=json.loads(current_user.form_data or '{}'))
    else:
        print("lol")
        return render_template('FinancialCalculator.html', form_data=json.loads(current_user.form_data or '{}'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('calculator'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session.pop('form_data', None)  # Add this line to clear session data
            return redirect(url_for('calculator'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    if request.method == 'POST':
        form_data = request.form

        # Perform calculations and return results
        conservative_savings, moderate_savings, aggressive_savings, recommendations = calculate_savings(form_data)

        return render_template('results.html', conservative_savings=conservative_savings, moderate_savings=moderate_savings, aggressive_savings=aggressive_savings, recommendations=recommendations)
    else:
        return redirect(url_for('calculator'))

def calculate_savings(form_data):
    current_age = int(form_data['current_age'])
    desired_age = int(form_data['desired_age'])
    current_savings = float(form_data['current_savings'])
    annual_contributions = float(form_data['annual_contributions'])
    desired_net_worth = float(form_data['desired_net_worth'])

    investment_strategies = {
        'Conservative': 0.04,
        'Moderate': 0.06,
        'Aggressive': 0.08
    }

    years_to_retirement = desired_age - current_age
    savings = {}
    for strategy, rate in investment_strategies.items():
        future_value = current_savings * (1 + rate) ** years_to_retirement + \
                    annual_contributions * ((1 + rate) ** years_to_retirement - 1) / rate
        savings[strategy] = future_value

    recommendations = f"To achieve a net worth of ${desired_net_worth} by retirement, "
    if savings['Aggressive'] >= desired_net_worth:
        recommendations += "you should choose the Aggressive strategy."
    elif savings['Moderate'] >= desired_net_worth:
        recommendations += "you can choose either the Moderate or Aggressive strategy."
    elif savings['Conservative'] >= desired_net_worth:
        recommendations += "you can follow any of the three investment strategies."
    else:
        required_rate = (desired_net_worth - current_savings) / (annual_contributions * years_to_retirement)
        recommendations += f"you need to increase your annual contributions or aim for an annual return higher than {required_rate * 100:.2f}%."

    return savings['Conservative'], savings['Moderate'], savings['Aggressive'], recommendations


if __name__ == "__main__":
    app.run(debug=True)


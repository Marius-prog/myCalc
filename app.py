from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from commands import add, subtract, multiply, divide
from validations import validate_number

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Calculator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    firstNumber = db.Column(db.Float, nullable=True)
    secondNumber = db.Column(db.Float, nullable=True)
    operation = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Calculator('{self.name}', '{self.firstNumber}', '{self.secondNumber}', '{self.operation}', '{self.date_created}')"


@app.route("/")
def index():
    return render_template("app.html")


def save_to_database(record: Calculator) -> str:
    try:
        db.session.add(record)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'


def update_database(record: Calculator) -> str:
    try:
        # TODO: update
        # db.session.
        db.session.add(record)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'


def get_from_database(id: int) -> Calculator:
    record = Calculator.query.get_or_404(id)
    if record is None:
        pass

    return record


@app.route("/first", methods=["POST"])
def post_first_number():
    print("pirmas")
    number = request.form["number"]
    validate_number(number)
    save_to_database(Calculator(first_number=number))


@app.route("/second", methods=["POST"])
def post_second_number():
    print("antras")
    number = request.form["number"]
    validate_number(number)
    save_to_database(Calculator(second_number=number))


@app.route("/operation", methods=["POST"])
def post_operation_number():
    print("operation")
    operation = request.form.get["operation"]
    save_to_database(Calculator(operation=operation))


@app.route("/calculate")
def get_result(id: int):
    record = get_from_database(id)
    if record.operation == "add":
        result = add(1, 5)
    elif record.operation == "subtract":
        result = subtract(1, 2)
    elif record.operation == "multiply":
        result = multiply(1, 2)
    else:
        result = divide(1, 2)
    return result


@app.errorhandler(404)
def error(error):
    return render_template("index.html", error=error), 404


if __name__ == "__main__":
    app.run(debug=True, port=2000)

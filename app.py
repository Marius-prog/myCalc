from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from commands import add, subtract, multiply, divide
from validations import validate_number

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    calculations = db.relationship("Calculation", backref="owner")


class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstNumber = db.Column(db.Float, nullable=False)
    secondNumber = db.Column(db.Float, nullable=False)
    operation = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))


@app.route("/")
def index():
    return render_template("app.html")


def save_to_database(record: Calculation) -> str:
    try:
        db.session.add(record)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'


def update_database(record: Calculation) -> str:
    try:
        # TODO: update
        # db.session.
        # record = ....
        db.session.add(record)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'


def get_from_database(id) -> Calculation:
    record = Calculation.query.get_or_404(id)
    if record is None:
        pass

    return record


@app.route("/first", methods=["POST"])
def post_first_number():
    print("pirmas")
    number = request.form["number"]
    validate_number(number)
    save_to_database(Calculation(first_number=number))
    return render_template('app.html', number=number)


@app.route("/second", methods=["POST"])
def post_second_number():
    print("antras")
    number = request.form["number"]
    validate_number(number)
    save_to_database(Calculation(second_number=number))
    return render_template('app.html', number=number)


@app.route("/operation", methods=["POST"])
def post_operation_number():
    print("operation")
    operation = request.form.get["operation"]
    save_to_database(Calculation(operation=operation))
    return render_template('app.html', operation=operation)


@app.route("/calculate")
def get_result(id):
    record = get_from_database(id)
    if record.operation == "add":
        result = add(1, 5)
    elif record.operation == "subtract":
        result = subtract(1, 2)
    elif record.operation == "multiply":
        result = multiply(1, 2)
    else:
        result = divide(1, 2)
    return render_template('app.html', record=record, result=result)


# @app.errorhandler(404)
# def error(error):
#     return render_template("index.html", error=error), 404


if __name__ == "__main__":
    app.run(debug=True, port=2000)

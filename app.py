from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ecyillztfyrtqs:3f94d910a172ba187593dc19dd45ef9a4a6af9109b187cc9aee7d8c2120e9656@ec2-34-230-231-71.compute-1.amazonaws.com:5432/dea3rjmml8rrnh"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)


class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True, nullable=False)
    month = db.Column(db.String(), nullable=False)
    daysInMonth = db.Column(db.Integer, nullable=False)
    daysInPreviousMonth = db.Column(db.Integer, nullable=False)
    startDay = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, position, month, daysInMonth, daysInPreviousMonth, startDay, year):
        self.position = position
        self.month = month
        self.daysInMonth = daysInMonth
        self.daysInPreviousMonth = daysInPreviousMonth
        self.startDay = startDay
        self.year = year

class MonthSchema(ma.Schema):
    class Meta:
        fields = ("id", "position", "month", "daysInMonth", "daysInPreviousMonth", "startDay", "year")

month_schema = MonthSchema()
multiple_month_schema = MonthSchema(many=True)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, text, date, month, year):
        self.text = text
        self.date = date
        self.month = month
        self.year = year

class ReminderSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "date", "month", "year")

reminder_schema = ReminderSchema()
multiple_reminder_schema = ReminderSchema(many=True)


@app.route("/month/add", methods=["POST"])
def add_month():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")
    
    post_data = request.get_json()
    position = post_data.get("position")
    month = post_data.get("month")
    daysInMonth = post_data.get("daysInMonth")
    daysInPreviousMonth = post_data.get("daysInPreviousMonth")
    startDay = post_data.get("startDay")
    year = post_data.get("year")

    record = Month(position, month, daysInMonth, daysInPreviousMonth, startDay, year)
    db.session.add(record)
    db.session.commit()

    return jsonify("Month added successfully")

@app.route("/month/get", methods=["GET"])
def get_all_months():
    all_months = db.session.query(Month).all()
    return jsonify(multiple_month_schema.dump(all_months))

@app.route("/reminder/add", methods=["POST"])
def add_reminder():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    text = post_data.get("text")
    date = post_data.get("date")
    month = post_data.get("month")
    year = post_data.get("year")

    record = Reminder(text, date, month, year)
    db.session.add(record)
    db.session.commit()

    return jsonify("Reminder added successfully")

@app.route("/reminder/get", methods=["GET"])
def get_all_reminders():
    all_reminders = db.session.query(Reminder).all()
    return jsonify(multiple_reminder_schema.dump(all_reminders))

@app.route("/reminder/get/<date>/<month>/<year>", methods=["GET"])
def get_one_reminder(date, month, year):
    reminder = db.session.query(Reminder).filter(Reminder.date == date).filter(Reminder.month == month).filter(Reminder.year == year).first()

    return jsonify(reminder_schema.dump(reminder))

@app.route("/reminder/update", methods=["PUT"])
def update_reminder():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    put_data = request.get_json()
    text = put_data.get("text")
    date = put_data.get("date")
    month = put_data.get("month")
    year = put_data.get("year")

    reminder = db.session.query(Reminder).filter(Reminder.date == date).filter(Reminder.month == month).filter(Reminder.year == year).first()
    reminder.text = text
    db.session.commit()

    return jsonify("Reminder updated")

@app.route("/reminder/delete", methods=["DELETE"])
def delete_reminder():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    delete_data = request.get_json()
    date = delete_data.get("date")
    month = delete_data.get("month")
    year = delete_data.get("year")

    reminder = db.session.query(Reminder).filter(Reminder.date == date).filter(Reminder.month == month).filter(Reminder.year == year).first()
    db.session.delete(reminder)
    db.session.commit()

    return jsonify("Reminder deleted")

if __name__ == "__main__":
    app.run(debug=True)
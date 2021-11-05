from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import pymysql
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('db_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('secretkey')

db = SQLAlchemy(app)

class Employee(db.Model):
    empno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    salary = db.Column(db.Integer)
    marks = db.Column(db.Integer)
    subject = db.Column(db.String(50))
    dept = db.Column(db.String(50))

db.drop_all()
db.create_all()

@app.route('/')
def home():
    emps = Employee.query.all()
    return render_template('Homepage.html', records=emps)

@app.route('/editRecord/<int:empno>')
def editRecordForm(empno):
    emp = Employee.query.filter_by(empno=empno).first()
    return render_template('EditForm.html', record=emp)

@app.route("/saveEditedRecord", methods=["POST"])
def saveEditedRecord():
    empno=request.form["empno"]
    name=request.form["na"]
    department=request.form["dept"]
    salary=request.form["sal"]
    subject=request.form["subject"]
    marks=request.form["marks"]
    emp = Employee.query.filter_by(empno=empno).first()
    emp.name = name
    emp.salary = salary
    emp.dept = department
    emp.subject = subject
    emp.marks = marks
    db.session.commit()
    return redirect("/")


@app.route("/filterrecords",methods=["POST"])
def filterrecords():
    if request.form["dept"]=="all":
        return redirect("/")
    else:
        data = Employee.query.filter_by(dept=request.form["dept"]).all()
        return render_template("Homepage.html",records=data)
	


@app.route("/addnewRecord")
def addNewRecord():
	return render_template("inputform.html")

@app.route("/saveRecord",methods=["POST"])
def saveRecord():
    name=request.form["na"]
    department=request.form["dept"]
    salary=request.form["sal"]
    subject=request.form["subject"]
    marks=request.form["marks"]
    newemp = Employee(name=name, dept=department, salary=salary, subject=subject, marks=marks)
    db.session.add(newemp)
    db.session.commit()
    return redirect("/")

@app.route("/personaldetails/<int:empno>")
def personalInformation(empno):
	data = Employee.query.filter_by(empno=empno).first()
	return render_template("personalinforamtion.html",record=data)

@app.route("/deleteEmployee/<int:empno>")
def deleteEmployee(empno):
    emp = Employee.query.filter_by(empno=empno).first()
    db.session.delete(emp)
    db.session.commit()
    return redirect("/")

app.run(debug=True, host='0.0.0.0')

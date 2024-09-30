"""
Luiz:

Login
Register student
Schedule

Kelvin:

Dashboard
Register class
Schedule classrooms

Matiele:

MainFrame
Register classrooms

Rafael:

Register build
Schedule classrooms
"""

from flask import Flask, render_template
from app import app

@app.route('/schedule/classrooms', methods=[('POST')])
def schedule_classroom():
    return render_template('codigo.html')

@app.route('/register-build', methods=[('POST')])
def register_build():
    return render_template('codigo.html')
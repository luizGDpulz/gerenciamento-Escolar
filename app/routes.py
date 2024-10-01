"""
Luiz:

Login
Register student
Schedule

Kelvin:

Dashboard
Register class
Schedule classrooms

Matielii:

MainFrame
Register classrooms



Rafael:

Register build
Schedule classrooms
"""

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/register-classroom', methods=['POST'])
def register_classroom():
    return render_template('codigo.html')



@app.route('/mainframe', methods=['POST'])
def mainframe():
    return render_template('codigo.html')

   
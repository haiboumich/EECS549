from flask import jsonify, request, Flask, Blueprint
from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import hash

login = Blueprint('login', __name__, template_folder='templates')

db = extensions.connect_to_database()

@login.route("/login", methods = ['POST'])
def login_route():
    if request.method == "POST":
        data = request.get_json()

        if len(data) < 2:
            errorDict = {
                "errors": [
                    {
                        "message": "You did not provide the necessary fields"
                    }
                ]
            }

            return jsonify(errorDict), 422

        username = data['username']
        password = data['password']

        cur1 = db.cursor()
        cur1.execute('SELECT username FROM User')
        results1 = cur1.fetchall()
        same = 0
        for user in results1:
            if user['username'] == username:
                same += 1
        if same == 0:
            errorDict = {
                "errors": [
                    {
                        "message": "Username does not exist"
                    }
                ]
            }

            return jsonify(errorDict), 404

        cur2 = db.cursor()
        cur2.execute('SELECT password, firstname, lastname FROM User WHERE username = %s', (username, ))
        results2 = cur2.fetchall()
        firstname = ''
        lastname = ''
        for res in results2: 
            firstname = res['firstname']
            lastname = res['lastname']
            salt = hash.getSalt(res['password'])
            hashPassword = hash.hashPasswordWithSalt(password, salt)

            if res['password'] != hashPassword:
                errorDict = {
                    "errors": [
                        {
                            "message": "Password is incorrect for the specified username"
                        }
                    ]
                }

                return jsonify(errorDict), 422

        session['username'] = username
        session['firstname'] = firstname
        session['lastname'] = lastname

        userDict = {
            "username": username
        }

        return jsonify(userDict)
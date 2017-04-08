from flask import Flask, session, escape, request, Blueprint, render_template, jsonify, json
import MySQLdb
import MySQLdb.cursors
from extensions import *
import config
import hash

signup = Blueprint('signup', __name__, template_folder='templates')

db = connect_to_database()

@signup.route("/signup", methods = ['GET', 'POST', 'PUT'])
def signup_route():
    if request.method == "GET":
        if 'username' in session:
            username = session['username']
            #print "fuck      username=", username
            cur1 = db.cursor()
            cur1.execute('SELECT firstname, lastname, email FROM User WHERE username = %s', (username, ))
            results1 = cur1.fetchall()
            firstname = ''
            lastname = ''
            email = ''
            #print "fuck2      username=", username
            for user in results1:
                firstname = user['firstname']
                lastname = user['lastname']
                email = user['email']
            #print "fuck3      username=", username
            userDict = {
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email
            }
            print "fuck4      username=", username
            return jsonify(userDict)
        
        print "fuck      username="
        errorDict = {
            "errors": [
                {
                    "message": "You do not have the necessary credentials for the resource"
                }
            ]
        }

        return jsonify(errorDict), 401

    elif request.method == "POST":
        
        data = request.get_json()

        if len(data) < 6:
            errorDict = {
                "errors": [
                    {
                        "message": "You did not provide the necessary fields"
                    }
                ]
            }
            print "fuck !!!!!!!!!"

            return jsonify(errorDict), 422

        #isUsernameEmpty == True or isPassword1Empty == True or isPassword2Empty == True or isEmailEmpty == True
        '''if username == '' or password1 == '' or password2 == '' or email == '':
            errorDict = {
                "errors": [
                        {
                            "message": "You did not provide the necessary fields"
                        }
                    ]
            }

            return jsonify(errorDict), 422'''

        username = data['username']
        firstname = data['firstname']
        lastname = data['lastname']
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']
            
        errorDict = {
            "errors": [

            ]
        }

        #isUsernameRepeated == True
        cur2 = db.cursor()
        cur2.execute('SELECT username FROM User')
        results2 = cur2.fetchall()
        for res2 in results2:
            if res2['username'] == username:
                mesDict = {
                    "message": "This username is taken"
                }
                errorDict["errors"].append(mesDict)

        #isUsernameTooShort == True
        if isStrLengthLessThanN(username, 2):
            mesDict = {
                "message": "Usernames must be at least 3 characters long"
            }
            errorDict["errors"].append(mesDict)

        #isUsernameCharIllegal == True
        if not isStrAllLDU(username):
            mesDict = {
                "message": "Usernames may only contain letters, digits, and underscores"
            }
            errorDict["errors"].append(mesDict)

        #isPassword1TooShort == True
        if isStrLengthLessThanN(password1, 7):
            mesDict = {
                "message": "Passwords must be at least 8 characters long"
            }
            errorDict["errors"].append(mesDict)

        #isPassword1DigitLetterIllegal == True
        if not ifStrHasDL(password1):
            mesDict = {
                "message": "Passwords must contain at least one letter and one number"
            }
            errorDict["errors"].append(mesDict)

        #isPassword1CharIllegal == True
        if not isStrAllLDU(password1):
            mesDict = {
                "message": "Passwords may only contain letters, digits, and underscores"
            }
            errorDict["errors"].append(mesDict)

        #isPassword12Mismatch == True
        if not password1 == password2:
            mesDict = {
                "message": "Passwords do not match"
            }
            errorDict["errors"].append(mesDict)

        #isEmailIllegal == True
        if not isEmailValid(email):
            mesDict = {
                "message": "Email address must be valid"
            }
            errorDict["errors"].append(mesDict)

        #isUsernameTooLong == True
        if not isStrLengthLessThanN(username, 20):
            mesDict = {
                "message": "Username must be no longer than 20 characters"
            }
            errorDict["errors"].append(mesDict)

        #isFirstnameTooLong == True
        if not isStrLengthLessThanN(firstname, 20):
            mesDict = {
                "message": "Firstname must be no longer than 20 characters"
            }
            errorDict["errors"].append(mesDict)

        #isLastnameTooLong == True
        if not isStrLengthLessThanN(lastname, 20):
            mesDict = {
                "message": "Lastname must be no longer than 20 characters"
            }
            errorDict["errors"].append(mesDict)
        
        #isEmailTooLong == True
        if not isStrLengthLessThanN(email, 40):
            mesDict = {
                "message": "Email must be no longer than 40 characters"
            }
            errorDict["errors"].append(mesDict)
        
        if not len(errorDict["errors"]) == 0:
            return jsonify(errorDict), 422
        
        hashPassword = hash.hashPassword(password1)
        
        cur3 = db.cursor()
        add_user = ("INSERT INTO User (username, firstname, lastname, password, email) VALUES (%s, %s, %s, %s, %s)")
        data_user = (username, firstname, lastname, hashPassword, email)
        cur3.execute(add_user, data_user)

        cur4 = db.cursor()
        cur4.execute("SELECT albumid FROM Album WHERE access = 'public'")
        results4 = cur4.fetchall()

        for album in results4:
            cur5 = db.cursor()
            add_access = ("INSERT INTO AlbumAccess (albumid, username) VALUES (%s, %s)")
            data_access = (album['albumid'], username)
            cur5.execute(add_access, data_access)

        userDict = {
                "username": username,
                "firstname": firstname,
                "lastname": lastname,
                "email": email
        }

        return jsonify(userDict), 201

    elif request.method == "PUT":
        if 'username' in session:
            data = request.get_json()
            username = data['username']
            firstname = data['firstname']
            lastname = data['lastname']
            password1 = data['password1']
            password2 = data['password2']
            email = data['email']

            if not username == session['username']:
                errorDict = {
                    "errors": [
                        {
                            "message": "You do not have the necessary permissions for the resource"
                        }
                    ]
                }

                return jsonify(errorDict), 403

            errorDict = {
                "errors": [

                ]
            }

            #isEmailIllegal == True
            if not isEmailValid(email):
                mesDict = {
                    "message": "Email address must be valid"
                }
                errorDict["errors"].append(mesDict)

            #isFirstnameTooLong == True
            if not isStrLengthLessThanN(firstname, 20):
                mesDict = {
                    "message": "Firstname must be no longer than 20 characters"
                }
                errorDict["errors"].append(mesDict)

            #isLastnameTooLong == True
            if not isStrLengthLessThanN(lastname, 20):
                mesDict = {
                    "message": "Lastname must be no longer than 20 characters"
                }
                errorDict["errors"].append(mesDict)
            
            #isEmailTooLong == True
            if not isStrLengthLessThanN(email, 40):
                mesDict = {
                    "message": "Email must be no longer than 40 characters"
                }
                errorDict["errors"].append(mesDict)

            if password1 == '' and password2 == '':
                if not len(errorDict["errors"]) == 0:
                    return jsonify(errorDict), 422 
                else:
                    cur6 = db.cursor()
                    cur6.execute('UPDATE User SET firstname = %s, lastname = %s, email = %s WHERE username = %s', (firstname, lastname, email, username))
            else:
                #isPassword1TooShort == True
                if isStrLengthLessThanN(password1, 7):
                    mesDict = {
                        "message": "Passwords must be at least 8 characters long"
                    }
                    errorDict["errors"].append(mesDict)

                #isPassword1DigitLetterIllegal == True
                if not ifStrHasDL(password1):
                    mesDict = {
                        "message": "Passwords must contain at least one letter and one number"
                    }
                    errorDict["errors"].append(mesDict)

                #isPassword1CharIllegal == True
                if not isStrAllLDU(password1):
                    mesDict = {
                        "message": "Passwords may only contain letters, digits, and underscores"
                    }
                    errorDict["errors"].append(mesDict)

                #isPassword12Mismatch == True
                if not password1 == password2:
                    mesDict = {
                        "message": "Passwords do not match"
                    }
                    errorDict["errors"].append(mesDict)

                if not len(errorDict["errors"]) == 0:
                    return jsonify(errorDict), 422
                    
                else: 
                    hashPassword = hash.hashPassword(password1)

                    cur7 = db.cursor()
                    cur7.execute('UPDATE User SET firstname = %s, lastname = %s, password = %s, email = %s WHERE username = %s', (firstname, lastname, hashPassword, email, username))

            userDict = {
                    "username": username,
                    "firstname": firstname,
                    "lastname": lastname,
                    "email": email
            }

            return jsonify(userDict), 201

        errorDict = {
            "errors": [
                {
                    "message": "You do not have the necessary credentials for the resource"
                }
            ]
        }

        return jsonify(errorDict), 401

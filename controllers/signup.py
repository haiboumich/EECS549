from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
import MySQLdb
import MySQLdb.cursors
from extensions import *
import config
import hash

signup = Blueprint('signup', __name__, template_folder='templates')

db = connect_to_database()

@signup.route('/signup', methods = ['GET', 'POST'])
def signup_route():
    if 'username' in session:
        return redirect(url_for('user.user_route'))
    
    if request.method == 'POST':

        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        
        isUsernameRepeated = False
        isPassword1TooShort = False
        isPassword12Mismatch = False
        
        cur1 = db.cursor()
        cur1.execute('SELECT username FROM UserInfo')
        result1 = cur1.fetchall()
        for user in result1:
            if user['username'] == username:
                isUsernameRepeated = True
                
        if not password1 == password2:
            isPassword12Mismatch = True

        if isStrLengthLessThanN(password1, 7):
            isPassword1TooShort = True
        
        options = {
            "edit" :False,
            "method" :'POST',
            "isUsernameRepeated": isUsernameRepeated,
            "isPassword1TooShort": isPassword1TooShort,
            "isPassword12Mismatch": isPassword12Mismatch
        }
        for key in options:
            if options[key] == True:
                return render_template("signup.html", **options)
        
        hashPassword = hash.hashPassword(password1)
        
        cur2 = db.cursor()
        add_user = ("INSERT INTO UserInfo (username, firstname, lastname, password, email) VALUES (%s, %s, %s, %s, %s)")
        data_user = (username, firstname, lastname, hashPassword, email)
        cur2.execute(add_user, data_user)
        return redirect(url_for('login.login_route'))
    
    options = {
        "edit" : False,
        "method" : 'GET'     
    }
    return render_template("signup.html", **options)    

    
@signup.route('/signup/edit', methods = ['GET', 'POST'])
def signup_edit_route():
    if not 'username' in session:
        return redirect(url_for('login.login_route'))

    username = session['username']
    cur7 = db.cursor()
    cur7.execute('SELECT firstname, lastname, email FROM UserInfo WHERE username = %s', (username, ))
    results7 = cur7.fetchall()
    
    if request.method == 'POST':
        #firstname = request.form['firstname'].encode('ascii','ignore')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        isPassword12Mismatch = False

        if not password1 == password2:
            isPassword12Mismatch = True

        if isStrLengthLessThanN(password1, 7):
            isPassword1TooShort = True

        options = {
            "edit" : True,
            "login": True,
            "method" : 'POST',
            "isPassword1TooShort": isPassword1TooShort,
            "isPassword12Mismatch": isPassword12Mismatch,
            "Name":results7
        }
        
        if options['isPassword1TooShort'] or options['isPassword12Mismatch']:
            return render_template("signup.html", **options)

        cur1 = db.cursor()
        cur1.execute('UPDATE UserInfo SET firstname = %s, lastname = %s, email = %s, password = %s WHERE username = %s', (firstname, lastname, email, password, username))
        return redirect(url_for('signup.signup_edit_route'))

    options = {
        "edit" : True,
        "login": True,
        "method" : 'GET', 
        "Name":results7
    }
    return render_template("signup.html", **options)

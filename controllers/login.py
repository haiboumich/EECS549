from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import hash

login = Blueprint('login', __name__, template_folder='templates')

db = extensions.connect_to_database()

@login.route('/login', methods = ['GET', 'POST'])
def login_route():
    options = {
        "isUsernameEmpty": False,
        "isPasswordEmpty": False,
        "isUsernameWrong": False,
        "isPassowrdWrong": False
    }
    if request.method == 'POST':
        '''if not 'username' in request.args or not 'password' in request.args:
            if not 'username' in request.args:
                options['isUsernameEmpty'] = True
            if not 'password' in request.args:
                options['isPasswordEmpty'] = True
            return render_template("login.html", **options)'''
        
        username = request.form['username']
        passwordLogin = request.form['password']

    

        #print "username = ", username
        #print "passwordLogin = ", passwordLogin


        #print "username = ", username
        #print "passwordLogin = ", passwordLogin
        
        if username == '' or passwordLogin == '':
            if username == '':
                options['isUsernameEmpty'] = True
            if passwordLogin == '':
                options['isPasswordEmpty'] = True
            return render_template("login.html", **options)
        
        cur1 = db.cursor()
        cur1.execute('SELECT username FROM UserInfo')
        results1 = cur1.fetchall()
        same = 0
        for user in results1:
            if user['username'] == username:
                same += 1
        if same == 0:
            options['isUsernameWrong'] = True
        if options['isUsernameWrong']:
            return render_template("login.html", **options)
        
        
        cur2 = db.cursor()
        cur2.execute('SELECT password FROM UserInfo WHERE username = %s', (username, ))
        results2 = cur2.fetchall()
        for password in results2:
            #print 'passwordType=', type(password) 
            salt = hash.getSalt(password['password'])
            hashPassword = hash.hashPasswordWithSalt(passwordLogin, salt)

            
            #print "hashPassword = ", hashPassword
            #print "password['password'] = ", password['password']

            if password['password'] != hashPassword:
                options['isPassowrdWrong'] = True
        if options['isPassowrdWrong']:
            return render_template("login.html", **options)

        #print "password check right"

        #both username and password is correct
        if 'username' in session:
            session.pop('username', None)
        
        session['username'] = username
        return redirect(url_for('main.main_route'))
        
    return render_template("login.html")

  



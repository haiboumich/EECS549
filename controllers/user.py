from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config

user = Blueprint('user', __name__, template_folder='templates')

db = extensions.connect_to_database()

@user.route('/user', methods = ['GET', 'POST'])
def user_route():
	if 'username' in session:
		username = session['username']

		options = {
			"edit": False,
			"username": username
		}
		return render_template("user.html", **options)

	return redirect(url_for('login.login_route'))

@user.route('/user/edit', methods = ['GET', 'POST'])
def user_edit_route():
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
			"Name":results7,
			"username": username
		}
		
		if options['isPassword1TooShort'] == False and options['isPassword12Mismatch'] == False:
			cur1 = db.cursor()
			cur1.execute('UPDATE UserInfo SET firstname = %s, lastname = %s, email = %s, password = %s WHERE username = %s', (firstname, lastname, email, password, username))

		return redirect(url_for('user.user_edit_route'))

	options = {
		"edit" : True,
		"login": True,
		"method" : 'GET', 
		"Name":results7,
		"username": username
	}
	return render_template("user.html", **options)


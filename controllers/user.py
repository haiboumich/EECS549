from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import json

user = Blueprint('user', __name__, template_folder='templates')

db = extensions.connect_to_database()

@user.route('/user', methods = ['GET', 'POST'])
def user_route():
	if 'username' in session:
		username = session['username']

		cur = db.cursor()
		cur.execute('SELECT restaurant FROM Favorite WHERE username = %s', (username, )) 
		results = cur.fetchall()

		restaurants=[]
		for res in results:
			restaurants.append(res['restaurant'])

		name = []
		address = []
		postal_code = []
		stars = []
		review_count = []
		city = []
		state = []
		category_list = []
		recommend = []
		name_rec = []
		address_rec = []
		postal_code_rec = []
		stars_rec = []
		review_count_rec = []
		city_rec = []
		state_rec = []
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)

			for restaurant in restaurants:
				for item in json_decode:
					if item.get('name') == restaurant:
						name.append(item.get('name'))
						address.append(item.get('address'))
						postal_code.append(item.get('postal_code'))
						stars.append(item.get('stars'))
						review_count.append(item.get('review_count'))
						city.append(item.get('city'))
						state.append(item.get('state'))
						categories = item.get('categories')
						for category in categories:
							if category not in category_list:
								category_list.append(category)

			for category in category_list:
				if len(recommend) == 10:
					break
				temp = []
				for item in json_decode:
					if category in item.get('categories'):
						temp.append(item)
				temp = sorted(temp, key=lambda k: k['stars'], reverse=True)
				if len(temp) == 0:
					continue
				elif len(temp) == 1:
					recommend.append(temp[0])
				else:
					recommend.append(temp[0])
					recommend.append(temp[1])
			for item in recommend:
				name_rec.append(item.get('name'))
				address_rec.append(item.get('address'))
				postal_code_rec.append(item.get('postal_code'))
				stars_rec.append(item.get('stars'))
				review_count_rec.append(item.get('review_count'))
				city_rec.append(item.get('city'))
				state_rec.append(item.get('state'))
				

		options = {
			"edit": False,
			"username": username,
			"name": name,
			"address": address,
			"zipcode": postal_code,
			"rating": stars,
			"reviewcount": review_count,
			"city": city,
			"state": state,
			"name_rec": name_rec,
			"address_rec": address_rec,
			"zipcode_rec": postal_code_rec,
			"rating_rec": stars_rec,
			"reviewcount_rec": review_count_rec,
			"city_rec": city_rec,
			"state_rec": state_rec,
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


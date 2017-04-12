# from sklearn.feature_extraction.text import TfidfVectorizer
# from numpy import array, dot
from flask import *
import extensions 
from flask import url_for
import json
import MySQLdb
import MySQLdb.cursors

restaurants = Blueprint('restaurants', __name__, template_folder='templates')

db = extensions.connect_to_database()

@restaurants.route('/restaurants', methods = ['GET', 'POST'])
def restaurants_route():
	if 'name' not in request.args:
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			lines = []
			for item in json_decode:
				lines.append(item)

			lines = sorted(lines, key=lambda k: k['stars'], reverse=True)

			i = 0
			name = []
			address = []
			postal_code = []
			stars = []
			review_count = []
			general = True
			city = []
			state = []
			for item in lines:
				name.append(item.get('name'))
				address.append(item.get('address'))
				postal_code.append(item.get('postal_code'))
				stars.append(item.get('stars'))
				review_count.append(item.get('review_count'))
				city.append(item.get('city'))
				state.append(item.get('state'))
				i += 1
				if i == 200:
					break
			print('items in file:')
			print(i)

			username = ''
			if "username" in session:
				username = session['username']

			options = {
				"general": general,
				"name": name,
				"address": address,
				"zipcode": postal_code,
				"rating": stars,
				"reviewcount": review_count,
				"city": city,
				"state": state,
				"username": username
			}
			return render_template("restaurants.html", **options)
	else:
		name = request.args.get('name')

		username = ''
		favourite = False
		if "username" in session:
			username = session['username']
			cur1 = db.cursor()
			cur1.execute('SELECT restaurant FROM Favorite WHERE username = %s', (username, ))
			results = cur1.fetchall()

			for res in results:
				if res['restaurant'] == name:
					favourite = True
			print(username)

		if request.method == 'POST':
			if 'username' not in session:
				return redirect(url_for('login.login_route'))

			if favourite == False:
				cur2 = db.cursor()
				cur2.execute("INSERT INTO Favorite (username, restaurant) VALUES (%s, %s)",(username, name))
				favourite = True 
			elif favourite == True:
				cur3 = db.cursor()
				cur3.execute("DELETE FROM Favorite WHERE restaurant=%s", (name, ))
				favourite = False
    		
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			businessid = ''
			neighborhood = ''
			address = ''
			city = ''
			state = ''
			zipcode = ''
			latitude = ''
			longitude = ''
			rating = ''
			reviewcount = ''
			isopen = ''
			attributes = ''
			categories = ''
			hours = ''
			general = False
			for item in json_decode:
				if item.get('name') == name:
					businessid = item.get('business_id')
					neighborhood = item.get('neighborhood')
					address = item.get('address')
					city = item.get('city')
					state = item.get('state')
					zipcode = item.get('postal_code')
					latitude = item.get('latitude')
					longitude = item.get('longitude')
					rating = item.get('stars')
					reviewcount = item.get('review_count')
					isopen = item.get('is_open')
					attributes = item.get('attributes')
					categories = item.get('categories')
					hours = item.get('hours')

			options = {
				"general": general,
				"name": name,
				"businessid": businessid,
				"neighborhood": neighborhood,
				"address": address,
				"city": city,
				"state": state,
				"zipcode": zipcode,
				"latitude": latitude,
				"longitude": longitude,
				"rating": rating,
				"reviewcount": reviewcount,
				"isopen": isopen,
				"attributes": attributes,
				"categories": categories,
				"hours": hours,
				"favourite": favourite,
				"username": username
			}
		
			return render_template("restaurants.html", **options)
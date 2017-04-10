from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import array, dot
from flask import *
from extensions import connect_to_database
from flask import url_for
import json

restaurants = Blueprint('restaurants', __name__, template_folder='templates')

db = connect_to_database()

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
			options = {
				"general": general,
				"name": name,
				"address": address,
				"zipcode": postal_code,
				"rating": stars,
				"reviewcount": review_count,
				"city": city,
				"state": state
			}
			return render_template("restaurants.html", **options)
	else:
		name = request.args.get('name')

		favourite = False
		if request.method == 'POST':
			if not 'username' in session:
				return redirect(url_for('login.login_route'))

			username = session['username']
			cur1 = db.cursor()
			cur1.execute('SELECT favourites FROM UserInfo WHERE username = %s', (username, )) 
    		results1 = cur1.fetchall()
    		new_favourites = results1[0] + ',' + name
    		cur2 = db.cursor()
        	cur2.execute("UPDATE UserInfo SET favourites = %s WHERE username = %s",(new_favourites,username))
        	favourite = True 

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
			print(name)
			print(address)

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
				"favourite": favourite
			}
		
			return render_template("restaurants.html", **options)
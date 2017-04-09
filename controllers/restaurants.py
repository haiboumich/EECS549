from flask import *
from extensions import connect_to_database
from flask import url_for
import json

restaurants = Blueprint('restaurants', __name__, template_folder='templates')

# db = connect_to_database()

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
			for item in lines:
				name.append(item.get('name'))
				address.append(item.get('address'))
				postal_code.append(item.get('postal_code'))
				stars.append(item.get('stars'))
				review_count.append(item.get('review_count'))
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
			}
			return render_template("restaurants.html", **options)
	else:
		name = request.args.get('name')
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
				"hours": hours
			}
		
			return render_template("restaurants.html", **options)
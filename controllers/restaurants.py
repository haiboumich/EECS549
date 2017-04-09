from flask import *
from extensions import connect_to_database
from flask import url_for
import json

restaurants = Blueprint('restaurants', __name__, template_folder='templates')

# db = connect_to_database()

@restaurants.route('/restaurants', methods = ['GET', 'POST'])
def restaurants_route():
	with open('../business_LV.json', 'r') as inputFile:
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
			"name": name,
			"address": address,
			"zipcode": postal_code,
			"rating": stars,
			"reviewcount": review_count,
		}
		return render_template("restaurants.html", **options)
from flask import *
from extensions import connect_to_database
import json



search = Blueprint('search', __name__, template_folder = 'templates')

name_mat = extensions.get_name_mat()
address_mat = extensions.get_address_mat()

@search.route('/search', methods = ['GET', 'POST'])
def search_route():
	select = request.form.get('col')
	if select == "name":
		
	elif select == "address":

	elif select == "zipcode":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			list = []
			for item in json_decode:
				if select == item.get('postal_code'):
					list.append(item)
			list = sorted(list, key=lambda k: k['stars'], reverse=True)
			
			if len(list) == 0:
				outofrange = False
				options = {
					"outofrange": outofrange,
				}
				return render_template("search.html", **options)
			else:
				i = 0
				name = []
				address = []
				postal_code = []
				stars = []
				review_count = []
				outofrange = True
				for item in lines:
					name.append(item.get('name'))
					address.append(item.get('address'))
					postal_code.append(item.get('postal_code'))
					stars.append(item.get('stars'))
					review_count.append(item.get('review_count'))
					i += 1
					if i == min(200, len(list)):
						break
				options = {
					"outofrange": outofrange,
					"name": name,
					"address": address,
					"zipcode": postal_code,
					"rating": stars,
					"reviewcount": review_count,
				}
				return render_template("search.html", **options)
	elif select == "rating":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			list = []
			for item in json_decode:
				if select == item.get('stars'):
					list.append(item)
			
			if len(list) == 0:
				outofrange = False
				options = {
					"outofrange": outofrange,
				}
				return render_template("search.html", **options)
			else:
				i = 0
				name = []
				address = []
				postal_code = []
				stars = []
				review_count = []
				outofrange = True
				for item in lines:
					name.append(item.get('name'))
					address.append(item.get('address'))
					postal_code.append(item.get('postal_code'))
					stars.append(item.get('stars'))
					review_count.append(item.get('review_count'))
					i += 1
					if i == min(200, len(list)):
						break
				options = {
					"outofrange": outofrange,
					"name": name,
					"address": address,
					"zipcode": postal_code,
					"rating": stars,
					"reviewcount": review_count,
				}
				return render_template("search.html", **options)
	elif select == "reviewcount"
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			list = []
			for item in json_decode:
				if select == item.get('review_count'):
					list.append(item)
			list = sorted(list, key=lambda k: k['stars'], reverse=True)
			
			if len(list) == 0:
				outofrange = False
				options = {
					"outofrange": outofrange,
				}
				return render_template("search.html", **options)
			else:
				i = 0
				name = []
				address = []
				postal_code = []
				stars = []
				review_count = []
				outofrange = True
				for item in lines:
					name.append(item.get('name'))
					address.append(item.get('address'))
					postal_code.append(item.get('postal_code'))
					stars.append(item.get('stars'))
					review_count.append(item.get('review_count'))
					i += 1
					if i == min(200, len(list)):
						break
				options = {
					"outofrange": outofrange,
					"name": name,
					"address": address,
					"zipcode": postal_code,
					"rating": stars,
					"reviewcount": review_count,
				}
				return render_template("search.html", **options)
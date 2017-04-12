from flask import *
from sklearn.feature_extraction.text import TfidfVectorizer
from extensions import connect_to_database
import json
import sklearn.metrics.pairwise as smp

name_list = []
address_list = []
with open('business_LV.json', 'r') as inputFile:
	json_decode = json.load(inputFile)
	for item in json_decode:
		name_list.append(item.get('name'))
		address_list.append(item.get('address'))

name_vectorizer = TfidfVectorizer(min_df=1)
name_mat = name_vectorizer.fit_transform(name_list).toarray()
address_vectorizer = TfidfVectorizer(min_df=1)
address_mat = address_vectorizer.fit_transform(address_list).toarray()

search = Blueprint('search', __name__, template_folder = 'templates')

# name_mat = extensions.get_name_mat()
# address_mat = extensions.get_address_mat()

@search.route('/search', methods = ['GET', 'POST'])
def search_route():
	select = request.form.get('sort')
	if select == "name":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			score = smp.cosine_similarity(name_mat, name_vectorizer.transform([request.form.get('data')]))
			index = sorted(range(len(score)), key = lambda k:result[k], reverse = True)
			if score[index[0]] == 0:
				notfound = True
				options = {
					"notfound": notfound,
					"select": select,
					"value": request.form.get('data')
				}
				return render_template("search.html", **options)
			notfound = False
			i = 0
			name = []
			address = []
			postal_code = []
			stars = []
			review_count = []
			city = []
			state = []
			for idx in index:
				if score[idx] == 0:
					break
				else:
					name.append(json_decode[idx].get('name'))
					address.append(json_decode[idx].get('address'))
					postal_code.append(json_decode[idx].get('postal_code'))
					stars.append(json_decode[idx].get('stars'))
					review_count.append(json_decode[idx].get('review_count'))
					city.append(json_decode[idx].get('city'))
					state.append(json_decode[idx].get('state'))
					i += 1
					if i == 200:
						break
			options = {
				"notfound": notfound,
				"name": name,
				"address": address,
				"zipcode": postal_code,
				"rating": stars,
				"reviewcount": review_count,
				"city": city,
				"state": state
			}
			return render_template("search.html", **options)
	elif select == "address":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			score = smp.cosine_similarity(address_mat, address_vectorizer.transform([request.form.get('data')]))
			index = sorted(range(len(score)), key = lambda k:result[k], reverse = True)
			if score[index[0]] == 0:
				notfound = True
				options = {
					"notfound": notfound,
					"select": select,
					"value": request.form.get('data')
				}
				return render_template("search.html", **options)
			notfound = False
			i = 0
			name = []
			address = []
			postal_code = []
			stars = []
			review_count = []
			city = []
			state = []
			for idx in index:
				if score[idx] == 0:
					break
				else:
					name.append(json_decode[idx].get('name'))
					address.append(json_decode[idx].get('address'))
					postal_code.append(json_decode[idx].get('postal_code'))
					stars.append(json_decode[idx].get('stars'))
					review_count.append(json_decode[idx].get('review_count'))
					city.append(json_decode[idx].get('city'))
					state.append(json_decode[idx].get('state'))
					i += 1
					if i == 200:
						break
			options = {
				"notfound": notfound,
				"name": name,
				"address": address,
				"zipcode": postal_code,
				"rating": stars,
				"reviewcount": review_count,
				"city": city,
				"state": state
			}
			return render_template("search.html", **options)

	elif select == "zipcode":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			list = []
			for item in json_decode:
				if request.form.get('data') == item.get('postal_code'):
					list.append(item)
			list = sorted(list, key=lambda k: k['stars'], reverse=True)
			
			if len(list) == 0:
				outofrange = True
				options = {
					"outofrange": outofrange,
					"select": select,
					"value": request.form.get('data')
				}
				return render_template("search.html", **options)
			else:
				i = 0
				name = []
				address = []
				postal_code = []
				stars = []
				review_count = []
				outofrange = False
				city = []
				state = []
				for item in list:
					name.append(item.get('name'))
					address.append(item.get('address'))
					postal_code.append(item.get('postal_code'))
					stars.append(item.get('stars'))
					review_count.append(item.get('review_count'))
					city.append(item.get('city'))
					state.append(item.get('state'))
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
					"city": city,
					"state": state
				}
				return render_template("search.html", **options)

	elif select == "rating":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			list = []
			for item in json_decode:
				if float(request.form.get('data')) == float(item.get('stars')):
					list.append(item)
			list = sorted(list, key=lambda k: k['review_count'], reverse=True)
			
			if len(list) == 0:
				outofrange = True
				options = {
					"outofrange": outofrange,
					"select": select,
					"value": request.form.get('data')
				}
				return render_template("search.html", **options)
			else:
				i = 0
				name = []
				address = []
				postal_code = []
				stars = []
				review_count = []
				outofrange = False
				city = []
				state = []
				for item in list:
					name.append(item.get('name'))
					address.append(item.get('address'))
					postal_code.append(item.get('postal_code'))
					stars.append(item.get('stars'))
					review_count.append(item.get('review_count'))
					city.append(item.get('city'))
					state.append(item.get('state'))
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
					"city": city,
					"state": state
				}
				return render_template("search.html", **options)

	elif select == "reviewcount":
		with open('/vagrant/EECS549/business_LV.json', 'r') as inputFile:
			json_decode = json.load(inputFile)
			list = []
			for item in json_decode:
				if abs(int(request.form.get('data')) - int(item.get('review_count'))) < 15:
					list.append(item)
			list = sorted(list, key=lambda k: k['stars'], reverse=True)
			
			if len(list) == 0:
				outofrange = True
				options = {
					"outofrange": outofrange,
					"select": select,
					"value": request.form.get('data')
				}
				return render_template("search.html", **options)
			else:
				i = 0
				name = []
				address = []
				postal_code = []
				stars = []
				review_count = []
				outofrange = False
				city = []
				state = []
				for item in list:
					name.append(item.get('name'))
					address.append(item.get('address'))
					postal_code.append(item.get('postal_code'))
					stars.append(item.get('stars'))
					review_count.append(item.get('review_count'))
					city.append(item.get('city'))
					state.append(item.get('state'))
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
					"city": city,
					"state": state
				}
				return render_template("search.html", **options)
# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.metrics.pairwise as smp
from numpy import array, dot
import json

name_list = []
address_list = []
zipcode_list = []
rating_list = []
reviewcount_list = []
with open('business_LV.json', 'r') as inputFile:
	json_decode = json.load(inputFile)
	for item in json_decode:
		name_list.append(item.get('name'))
		address_list.append(item.get('address'))
		if item.get('postal_code') not in zipcode_list:
			zipcode_list.append(item.get('postal_code'))
		if item.get('stars') not in rating_list:
			rating_list.append(item.get('stars'))
		if item.get('review_count') not in reviewcount_list:
			reviewcount_list.append(item.get('review_count'))

# name_vectorizer = CountVectorizer(min_df=1)
# name_mat = name_vectorizer.fit_transform(name_list).toarray()
# address_vectorizer = CountVectorizer(min_df=1)
# address_mat = address_vectorizer.fit_transform(address_list).toarray()

# print(len(name_mat))
# print(len(address_mat))
# print(len(name_mat[0]))
# print(len(address_mat[0]))

# name_test = "buffet"

# result = smp.cosine_similarity(name_mat, name_vectorizer.transform([name_test]))

# print(len(result))
# print(len(result[0]))
# index = sorted(range(len(result)), key = lambda k:result[k])

print(sorted(zipcode_list))
print(sorted(rating_list))
print(sorted(reviewcount_list))
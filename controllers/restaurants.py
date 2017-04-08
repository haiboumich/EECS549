from flask import *
from extensions import connect_to_database
from flask import url_for

restaurants = Blueprint('restaurants', __name__, template_folder='templates')

db = connect_to_database()

@restaurants.route('/restaurants', methods = ['GET', 'POST'])
def restaurants_route():
	return render_template("restaurants.html")
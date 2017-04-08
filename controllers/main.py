from flask import *
from extensions import connect_to_database
from flask import url_for

main = Blueprint('main', __name__, template_folder='templates')

db = connect_to_database()

@main.route('/', methods = ['GET', 'POST'])
def main_route():
	return render_template("index.html")
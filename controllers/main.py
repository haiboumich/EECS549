from flask import *
import MySQLdb
import MySQLdb.cursors
import extensions
import config
import os
import hashlib
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import datetime
main = Blueprint('main', __name__, template_folder='templates')

db = extensions.connect_to_database()

@main.route('/')
def main_route():
    #[sensitive]
    login = False
    if 'username' in session:
        login = True
        username = session['username']
        options = {
            "login": login,
            "username": username,
        }
        #print login
        return render_template("index.html", **options)
    return render_template("index.html")
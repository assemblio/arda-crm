from flask import render_template
from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request

mod_home_page = Blueprint('home_page', __name__)


@mod_home_page.route('/', methods=['GET'])
def home_page():
    return render_template('index.html')

from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
mod_provided_services = Blueprint('provided_services', __name__, url_prefix='/services')


@mod_provided_services.route('', methods=['GET'])
def provided_services():
    pass

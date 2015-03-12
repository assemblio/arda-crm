from flask import Flask
import os
import ConfigParser
from flask.ext.pymongo import PyMongo
from logging.handlers import RotatingFileHandler

# Create MongoDB database object.
mongo = PyMongo()


def create_app():

    #Here we  create flask app
    app = Flask(__name__)

    #We load configurations
    load_config(app)

    #Configure logging
    configure_logging(app)

    #Import blueprint modules
    from arda.mod_auth.views import mod_auth
    from arda.mod_home_page.views import mod_home_page
    from arda.mod_customers.views import mod_customers
    from arda.mod_provided_services.views import mod_provided_services
    from arda.mod_admin.views import mod_admin

    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_home_page)
    app.register_blueprint(mod_customers)
    app.register_blueprint(mod_provided_services)
    app.register_blueprint(mod_admin)

    #Initialize the app to work with MongoDB
    mongo.init_app(app, config_prefix='MONGO')

    return app


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''
    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    app.config['USERNAME'] = config.get('Application', 'USERNAME')
    app.config['PASSWORD'] = config.get('Application', 'PASSWORD')
    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['BASE_PATH'] = config.get('Application', 'BASE_PATH')
    app.config['MONGO_DBNAME'] = config.get('Mongo', 'DB_NAME')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()

    # Set the secret key, keep this really secret.
    app.secret_key = config.get('Application', 'SECRET_KEY')


def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to. Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)

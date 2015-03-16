from flask import Flask
import os
import ConfigParser
from flask.ext.pymongo import PyMongo
from logging.handlers import RotatingFileHandler
from utils.utils import Utils
from flask.ext.bcrypt import Bcrypt
from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.mongoengine import MongoEngine, DoesNotExist
from flask.ext.login import LoginManager


#Here we  create flask app
app = Flask(__name__)

# Create MongoDB database object.
mongo = PyMongo()
utils = Utils()

bcrypt = Bcrypt()

# Create MongoDB instance
db = MongoEngine()

# Create Login Manager instance
login_manager = LoginManager()
# Initiate Login Manager
login_manager.init_app(app)

# Setup Flask-Security
from arda.mod_admin.models.user_model import Users, Role
user_datastore = MongoEngineUserDatastore(db, Users, Role)
security_ = Security(app, user_datastore)


def create_app():

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Instantiate MongoEngine instance
    db.init_app(app)

    # Create role "User" and "Admin"
    # Create the "admin" user with "admin" password
    create_user_roles(user_datastore)

    #Import blueprint modules
    from arda.mod_auth.views import mod_auth
    from arda.mod_home_page.views import mod_home_page
    from arda.mod_customers.views import mod_customers
    from arda.mod_services.views import mod_services
    from arda.mod_admin.views import mod_admin

    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_home_page)
    app.register_blueprint(mod_customers)
    app.register_blueprint(mod_services)
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

    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['MONGO_DBNAME'] = config.get('Mongo', 'DB_NAME')

    # Config MONGODB
    app.config['MONGODB_SETTINGS'] = {
        'db': config.get('MONGODB_SETTINGS', 'MONGODB_DATABASE'),
        'host': config.get('MONGODB_SETTINGS', 'MONGODB_HOST'),
        'port': int(config.get('MONGODB_SETTINGS', 'MONGODB_PORT'))
    }

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

    # First log informs where we are logging to.
    # Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)


def create_user_roles(user_datastore):
    '''
    Create the roles using the flask-security plugin.
    '''
    # Create User role
    try:
        Role.objects.get(name="Regular")
    except DoesNotExist:
        # Create the user role
        user_datastore.create_role(
            name='Regular',
            description='Regular user of the CRM.'
        )
    try:
        Role.objects.get(name="Admin")
    # Create Admin Role and admin user
    except DoesNotExist:
        # Create the admin role
        role = user_datastore.create_role(
            name='Admin',
            description='Admin of the CRM.'
        )
        try:
            Users.objects.get(email="admin@admin.com")
        # Create the admin user
        except DoesNotExist:
            user = user_datastore.create_user(
                email="admin@admin.com",
                password="$2a$10$o6k9L8RUiYkpaPF/Ym0freJbHzoDGTAxSP9cU8RgneDEGkas/5MSq",
                first_name="Filan",
                last_name="Fisteku"
            )
            user_datastore.add_role_to_user(user, role)

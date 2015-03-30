import argparse
from flask.ext.mongoengine import MongoEngine, DoesNotExist
from flask.ext.security import MongoEngineUserDatastore
from arda.mod_admin.models.user_model import Users, Role
from flask.ext.bcrypt import Bcrypt
from bson import ObjectId
# Create MongoDB instance
db = MongoEngine()
db.connect('arda')
bcrypt = Bcrypt()
user_datastore = MongoEngineUserDatastore(db, Users, Role)


def create_user(user_datastore, username, password):
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
                email=username,
                password=bcrypt.generate_password_hash(password, rounds=12),
                first_name="Filan",
                last_name="Fisteku",
                role="Admin",
                region="All",
            )
            user_datastore.add_role_to_user(user, role)


def create_initial_service():

    class Servicetypes(db.Document):
        id = db.StringField()
        serviceTypes = db.ListField()
        contactVia = db.ListField()


    Servicetypes(
        id = ObjectId('5509cb3b484d3f17a2409cea'),
        serviceTypes=[{
            "type": {
                "name": "Phone Call",
                "slug": "phone-call"
            },
            'serviceId': ObjectId(),
            "description": "Phone Call Service"
        },
        {
            "type": {
                "name": "E-mail",
                "slug": "e-mail"
            },
            'serviceId': ObjectId(),
            "description": "E-mail Service"
        },
        {
            "type": {
                "name": "Face-to-Face meeting",
                "slug": "face-to-face-meeting"
            },
            'serviceId': ObjectId(),
            "description": "Face-to-Face Service"
        }],
        contactVia = [{
            "type": {
                "name": "1",
                "slug": "1"
            },
            'contactId': ObjectId(),
            "description": "this one contact manner"
        },
        {
            "type": {
                "name": "2",
                "slug": "2"
            },
            'contactId': ObjectId(),
            "description": "this another contact manner"
        }]

        ).save()

# Run the app
if __name__ == '__main__':

    # Define the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='The admin username.')
    parser.add_argument('--password', help='The admin password.')

    # Parse arguemnts and run the app.
    args = parser.parse_args()
    username = args.username
    password = args.password
    create_user(user_datastore, username, password)
    create_initial_service()

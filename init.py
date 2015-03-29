import argparse
from flask.ext.mongoengine import MongoEngine

# Run the app
if __name__ == '__main__':

    # Define the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='The admin username.')
    parser.add_argument('--password', help='The admin password.')

    # Parse arguemnts and run the app.
    args = parser.parse_args()

    '''
        TODO:
            1) Create 'Regular' and 'Admin' roles.
            2) Create Admin user based on args.username and args.password.
            3) Create Services.
            4) Create Contacted Via.
    '''
    
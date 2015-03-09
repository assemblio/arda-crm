from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from arda import mongo
from arda.utils.utils import Utils
import json

utils = Utils()


mod_contacts_directory = Blueprint('contacts_directory', __name__, url_prefix='/contacts-page')


@mod_contacts_directory.route('', methods=['GET'])
def contacts():
    contacts_doc = mongo.db.contacts.find({})
    response = build_contacts_cursor(contacts_doc)

    return render_template('mod_contacts/contacts_directory.html', result=response)


@mod_contacts_directory.route('/new', methods=['GET', 'POST'])
def new_contact():
    from forms.contactsForm import ContactsForm
    form = ContactsForm()
    if request.method == "POST":
        contact_id = utils.get_doc_id()
        contacts_form = ContactsForm(request.form)
        contacts_doc = contacts_form.data
        mongo.db.contacts.update(
            {"_id": contact_id},
            {"$set": contacts_doc},
            True
        )
        return redirect('/contacts-page')

    return render_template('mod_contacts/new_contact.html', form=form)


def build_contacts_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []

    for idx, bp in enumerate(cursor):
        response_to_append_to.append(bp)

    return response

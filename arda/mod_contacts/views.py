from flask import Blueprint, render_template, \
                  session, redirect, url_for, current_app, request
from arda import mongo
from arda.utils.utils import Utils
import json
from forms.contactsForm import ContactsForm

utils = Utils()


mod_contacts_directory = Blueprint('contacts_directory', __name__, url_prefix='/contacts-page')


@mod_contacts_directory.route('', methods=['GET'])
def contacts():
    contacts_doc = mongo.db.contacts.find({})
    response = build_contacts_cursor(contacts_doc)

    return render_template('mod_contacts/contacts_directory.html', result=response)


@mod_contacts_directory.route('/new', methods=['GET', 'POST'])
def new_contact():
    form = ContactsForm()
    if request.method == "POST":
        #create an Id for the document we want to store
        costumer_id = utils.get_doc_id()
        #call the function which builds than stores the json document
        buld_save_costumer_document(costumer_id)
        return redirect('/contacts-page')

    return render_template('mod_contacts/new_contact.html', form=form)


def build_contacts_cursor(cursor):
    ''' Builds a JSON response for a given cursor
    '''
    response = json.loads('{}')
    response_to_append_to = response['results'] = []

    for idx, itm in enumerate(cursor):
        response_to_append_to.append(itm)

    return response


def buld_save_costumer_document(doc_id):

    contacts_form = ContactsForm(request.form)
    costumer = contacts_form.data

    json_obj = {}
    json_obj = {
        'company_name': costumer['company_name'],
        'first_name': costumer['first_name'],
        'last_name': costumer['last_name'],
        'costumer_type': costumer['costumer_type'],
        'job_title': costumer['job_title'],
        'phone': {
            'main_phone': costumer['main_phone'],
            'work_phone': costumer['work_phone'],
            'mobile': costumer['mobile'],
            'fax': costumer['fax'],
        },
        'address': {
            'billing': {
                'bill_add1': costumer['bill_add1'],
                'bill_add2': costumer['bill_add2'],
                'bill_city': costumer['bill_city'],
                'bill_state': costumer['bill_state'],
                'bill_postal_code': costumer['bill_postal_code'],
                'bill_country': costumer['bill_country'],
            },
            'shipping': {
                'ship_add1': costumer['ship_add1'],
                'ship_add2': costumer['ship_add2'],
                'ship_city': costumer['ship_city'],
                'ship_state': costumer['ship_state'],
                'ship_postal_code': costumer['ship_postal_code'],
                'ship_country': costumer['ship_country'],
            }
        },
        'email': costumer['email'],
        'website': costumer['website'],
        'provided_services': []
    }

    mongo.db.contacts.update(
        {'_id': doc_id},
        {'$set': json_obj},
        True
    )

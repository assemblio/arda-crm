from arda import db

class Billing(db.EmbeddedDocument):
    bill_add1 = db.StringField()
    bill_add2 = db.StringField()
    bill_city = db.StringField()
    bill_state = db.StringField()
    bill_postal_code = db.StringField()
    bill_country = db.StringField()

class Shipping(db.EmbeddedDocument):

    ship_add1 = db.StringField()
    ship_add2 = db.StringField()
    ship_city = db.StringField()
    ship_state = db.StringField()
    ship_postal_code = db.StringField()
    ship_country = db.StringField()

class Phone(db.EmbeddedDocument):
    main_phone = db.StringField()
    work_phone = db.StringField()
    mobile = db.StringField()
    fax = db.StringField()

class Address(db.EmbeddedDocument):

    billing = db.EmbeddedDocumentField(Billing)
    shipping = db.EmbeddedDocumentField(Shipping)

class Company(db.EmbeddedDocument):
    name = db.StringField()
    slug = db.StringField()

class First_Name(db.EmbeddedDocument):
    value = db.StringField()
    slug = db.StringField()

class Last_Name(db.EmbeddedDocument):
    value = db.StringField()
    slug = db.StringField()

class Costumer_Type(db.EmbeddedDocument):
    target_group = db.StringField()

class Customers(db.Document):
    company = db.EmbeddedDocumentField(Company)
    first_name = db.EmbeddedDocumentField(First_Name)
    last_name = db.EmbeddedDocumentField(Last_Name)
    costumer_type = db.EmbeddedDocumentField(Costumer_Type)
    job_title = db.StringField()
    region = db.StringField()
    phone = db.EmbeddedDocumentField(Phone)
    address = db.EmbeddedDocumentField(Address)
    email = db.StringField()
    website = db.StringField()
    provided_services = db.ListField()

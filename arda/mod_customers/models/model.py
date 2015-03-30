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


class Customer_Type(db.EmbeddedDocument):
    target_group = db.StringField()
    investor_size = db.StringField()
    business_name = db.StringField()
    vat = db.StringField()
    fiscal_number = db.StringField()
    legal_entity_types = db.StringField()
    industry = db.StringField()
    main_activity = db.StringField()
    founding_year = db.StringField()
    number_of_employees = db.StringField()
    size_category = db.StringField()
    investment = db.StringField()
    ngo_registration_number_ngo = db.StringField()
    vat_number_ngo = db.StringField()
    fiscal_number_ngo = db.StringField()
    sector_ngo = db.StringField()
    founding_year_ngo = db.StringField()
    number_of_staff_ngo = db.StringField()
    description_of_ngo = db.StringField()
    main_activities = db.StringField()
    donors = db.StringField()
    country = db.StringField()
    business = db.StringField()
    business_number = db.StringField()
    business_description = db.StringField()
    interest = db.StringField()
    investor_industry = db.StringField()
    industry_of_interest = db.StringField()
    investor_size = db.StringField()
    foundation_year_investor = db.StringField()
    municipality_name = db.StringField()
    department = db.StringField()
    offering = db.StringField()
    industries = db.StringField()
    modules = db.StringField()
    infrastructure_available = db.StringField()
    description = db.StringField()
    description_investor = db.StringField()


class Customers(db.Document):
    company = db.EmbeddedDocumentField(Company)
    first_name = db.EmbeddedDocumentField(First_Name)
    last_name = db.EmbeddedDocumentField(Last_Name)
    customer_type = db.EmbeddedDocumentField(Customer_Type)
    job_title = db.StringField()
    region = db.StringField()
    phone = db.EmbeddedDocumentField(Phone)
    address = db.EmbeddedDocumentField(Address)
    email = db.StringField()
    website = db.StringField()
    provided_services = db.ListField()

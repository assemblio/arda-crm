# -*- coding: UTF-8 -*-
from flask_wtf import Form
from wtforms import SelectField, TextField, RadioField, TextAreaField, BooleanField
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class CustomerForm(Form):

    municipalities = [
        'All', 'Prishtine', 'Drenas', 'Fushe Kosove', 'Obilliq', 'Podujeve',
        'Shtime', 'Gracanice', 'Lipjan',
        'All', 'Vushtrri', 'Zubin Potok', 'Zvecan', 'Leposavic', ' Mitrovice', 'Skenderaj',
        'All', 'Istog', 'Kline', ' Peja', 'Junik', 'Decan', 'Gjakova',
        'All', 'Prizren', 'Malisheva', 'Suhareka', 'Dragash', 'Mamusha', 'Rahovec',
        'All', 'Ferizaj', 'Gjilan', 'Viti', 'Novoberde', 'Kamenice', 'Hani Elezit', 'Kacanik',
        'Shterpce', 'Ranillug', 'Kllokot', 'Partesh'
    ]

    municipality = SelectField('Municipality', choices=[(x, x) for x in municipalities])
    municipality_region_central = SelectField('Municipality', choices=[(x, x) for x in municipalities[1:9]])
    municipality_region_north = SelectField('Municipality', choices=[(x, x) for x in municipalities[10:16]])
    municipality_region_west = SelectField('Municipality', choices=[(x, x) for x in municipalities[17:23]])
    municipality_region_south = SelectField('Municipality', choices=[(x, x) for x in municipalities[24:30]])
    municipality_region_east = SelectField('Municipality', choices=[(x, x) for x in municipalities[31:42]])

    search_municipality_region_central = SelectField('Municipality', choices=[(x, x) for x in municipalities[0:9]])
    search_municipality_region_north = SelectField('Municipality', choices=[(x, x) for x in municipalities[9:16]])
    search_municipality_region_west = SelectField('Municipality', choices=[(x, x) for x in municipalities[16:23]])
    search_municipality_region_south = SelectField('Municipality', choices=[(x, x) for x in municipalities[23:30]])
    search_municipality_region_east = SelectField('Municipality', choices=[(x, x) for x in municipalities[30:42]])

    arda_regions = ['North', 'East', 'West', 'South', 'Center']
    choices = [(x, x) for x in arda_regions]
    region = SelectField("Region", choices=choices)

    follow_up = TextField('Date to Follow-up')
    future_demand = BooleanField('Future Demand')
    category_of_request = TextField('Category of Request')
    #personal info
    company_name = TextField("Customer")
    first_name = TextField("First Name")
    last_name = TextField("Last Name")
    job_title = TextField("Job Title")
    main_phone = TextField("Main Phone")
    work_phone = TextField("Work Phone")
    mobile = TextField("Mobile Phone")
    fax = TextField("Fax")
    email = TextField("E-mail")
    website = TextField("Website")
    customer_address = TextAreaField('Adderess')
    customer_type = SelectField(
        "Customer Type",
        choices=[
            ('Business/Entrepreneur', 'Business/Entrepreneur'),
            ('Non-Governmental Organisation', 'Non-Governmental Organisation'),
            ('Investor', 'Investor'),
            ('Public Instituation', 'Public Instituation')
        ]
    )
    customer_industry = [
        '0510-0990 - Mining and quarrying',
        '1010-3320 - Manufacturing',
        '3510-3530 - Electricity, gas, steam and air conditioning supply',
        '3600 - 3900 - Water supply; sewerage, waste management and remediation activities',
        '4100 - 4390 - Construction',
        '4510 - 4799 - Wholesale and retail trade; repair of motor vehicles, motorcycles',
        '4911 - 5320 - Transport and storage',
        '5510 - 5630 - Accommodation and food activities',
        '5811 - 6399 - Information and Communication',
        '6411 - 6630 - Financin and Insurance Activities',
        '6811 - 6820 - Real Estate Activities',
        '6910 - 7500 - Professional, Scientific amd Technical Activities',
        '7710 - 8299 - Administrative and Support Service Activities',
        '8411 - 8430 - Public Administration and Defence; Compulsary social security',
        '8510 - 8550 - Education',
        '8610 - 8890 - Human and  Social Woreking Activities',
        '9000 - 9329 - Arts, Entertainment and Recreation',
        '9411 - 9609 - Other Service Activities',
        '9700 - 9820 - Activities of Households as Employers; Undifferentiated goods-and services producing activities of households for own use',
        '9900 - Activities of exteritorial organisations and bodies'
    ]

    #if Target Group is Business/Entrepreneur
    business_name = TextField("Business Name")
    vat = TextField("VAT Number")
    business_number = TextField("Business Number")
    fiscal_number = TextField("Fiscal Number")
    legal_entity_types = TextField("Legal Entity Type")
    industry = SelectField("Industry", choices=[(x, x) for x in customer_industry])
    main_activity = TextAreaField(" Business Dectription/Main Activity")
    founding_year = TextField("Founding Year")
    number_of_employees = TextField("Number of Employees")
    size_category = SelectField(
        "Size",
        choices=[
            ('Micro', 'Micro (1-9)'),
            ('Small', 'Small (10-49)'),
            ('Medium', 'Medium (50-249)'),
            ('Large', 'Large (250+)')
        ]
    )
    search_size_category = SelectField(
        "Size",
        choices=[
            ('All', 'All'),
            ('Micro', 'Micro (1-9)'),
            ('Small', 'Small (10-49)'),
            ('Medium', 'Medium (50-249)'),
            ('Large', 'Large (250+)')
        ]
    )
    investment = RadioField(
        "Interested in Invesment",
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ]
    )
    business_description = TextAreaField("Primary Interest for Cooperation")

    #Target Group: Investor
    business = TextField("Business")
    investor_business_number = TextField("Business Number")
    investor_vat = TextField("VAT Number")
    investor_fiscal_number = TextField("Fiscal Number")
    interest = TextField("Interest")
    investor_industry = TextField("Industry")
    industry_of_interest = TextField("Industry of interest")
    investor_size = TextField("Size")
    foundation_year_investor = TextField("Foundation Year")
    description_investor = TextAreaField("Business Description")

    department_choices = [
        'Department of Finance',
        'Department for Economic Development',
        'Department for Education',
        'Department for Health',
        'Department for Culture and Sport',
        'Department for Infrastructure',
        'Department for Public Services',
        'General Department of Cadaster',
        'Department of Administration',
        'Department of Inspections',
        'Department of Agriculture'
    ]
    #Target Group: Municipality
    municipality_name = TextField("Public Instituation Name")
    department = SelectField("Department", choices=[(x, x) for x in department_choices])
    offering = TextField("Offering")
    industries = TextField("Industries")
    modules = TextField("Modules")
    infrastructure_available = TextField("Infrastructure Available")
    investment_incentives = TextField("Investment Incentives")
    description = TextAreaField("Description")

    #if the Target Group is NGO
    ngo_registration_number_ngo = TextField("Registration Number")
    vat_number_ngo = TextField("VAT Number")
    fiscal_number_ngo = TextField("Fiscal Number")
    sector_ngo = TextField("Sector")
    founding_year_ngo = TextField("Founding Year")
    number_of_staff_ngo = TextField("Number of Staff")
    description_of_ngo = TextAreaField("Description")
    main_activities = TextField("Main Activities")
    donors = TextField("Donors")

    #Bill to Address fields
    bill_add1 = TextField("Invoice/Bill To Address:")
    bill_add2 = TextField("Invoice/Bill To Address ")
    bill_city = TextField("City")
    bill_state = TextField("State")
    bill_postal_code = TextField("Postal code")
    bill_country = TextField("Country")
    #Ship to Address fields
    ship_add1 = TextField("Ship to Address:")
    ship_add2 = TextField("Ship to Address")
    ship_city = TextField("City")
    ship_state = TextField("State")
    ship_postal_code = TextField("Postal code")
    ship_country = TextField("Country")

    country_list = [
        'Afghanistan','Åland Islands','Albania','Algeria','American Samoa','Andorra','Angola',
        'Anguilla','Antarctica','Antigua and Barbuda','Argentina','Armenia','Aruba','Australia',
        'Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium',
        'Belize','Benin','Bermuda','Bhutan','Bolivia','Bonaire, Sint Eustatius and Saba','Bosnia and Herzegovina',
        'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam',
        'Bulgaria','Burkina Faso','Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
        'Cayman Islands', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands',
        'Colombia', 'Comoros', 'Congo', 'Congo, the Democratic Republic of the Congo', 'Cook Islands',
        'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czech Republic',
        'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
        'Equatorial Guinea', 'Eritrea', 'Estonia', 'England', 'Ethiopia', 'Falkland Islands (Malvinas)',
        'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia',
        'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
        'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey',
        'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See (Vatican City State)', 'Honduras',
        'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland',
        'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan',
        'Kenya', 'Kiribati', 'Kosovo', "Korea, Democratic People's Republic of Korea", 'Korea',
        'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho',
        'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao',
        'Macedonia, the former Yugoslav Republic of Macedonia', 'Madagascar', 'Malawi', 'Malaysia',
        'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius',
        'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat',
        'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Northern Ireland', 'Netherlands', 'New Caledonia',
        'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands',
        'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay',
        'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania',
        'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha',
        'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon',
        'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe',
        'Saudi Arabia','Scotland', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)',
        'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands',
        'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen', 'Swaziland',
        'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan',
        'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago',
        'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine',
        'United Arab Emirates', 'United States', 'United States Minor Outlying Islands', 'Uruguay',
        'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of Venezuela', 'Viet Nam',
        'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wales', 'Wallis and Futuna', 'Western Sahara',
        'Yemen', 'Zambia', 'Zimbabwe'
    ]

    country = SelectField("Country", choices=[(x, x) for x in country_list])

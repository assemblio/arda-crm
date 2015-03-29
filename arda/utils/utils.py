from bson import ObjectId


class Utils(object):

    def __init__(self):
        pass

    def get_doc_id(self):
        ''' Get the doc_id.
        '''
        doc_id = str(ObjectId())

        return doc_id

    def get_default_settings(self):
        return {
            'site_title': 'CRM',
            'site_tagline': 'Just another CRM',
            'site_navbar_title': 'CRM',
            'web_url': '',
            'fb_url': '',
            'tw_url': '',
            'li_url': '',
        }

from arda import db
from flask.ext.security import UserMixin, RoleMixin
from bson import ObjectId

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Users(db.Document, UserMixin):
    first_name = db.StringField(max_length=255)
    last_name = db.StringField(max_length=255)
    region = db.StringField(max_length=255)
    email = db.StringField(max_length=255)
    password = db.StringField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])
    role = db.StringField()
    active = db.BooleanField(default=True)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<email {}'.format(self.email)

    def get_user(self, id):
        return Users.objects.get(id=id)

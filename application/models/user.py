from werkzeug.security import generate_password_hash
from application import db


class User(db.Model):
    """
    User Model - matches an user item from the database
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, index=True)
    last_name = db.Column(db.Text, index=True)
    username = db.Column(db.Text, unique=True, index=True)
    password = db.Column(db.Text)
    access_level_id = db.Column(db.Integer, db.ForeignKey('access_level.id'))

    def __init__(self, username='', password='', first_name='', last_name='', access_level_id=None):
        # force defaults in case None is sent
        self.first_name = first_name or ''
        self.last_name = last_name or ''
        self.username = username or ''
        self.password = generate_password_hash(password or '')
        self.access_level_id = access_level_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    @property
    def get_full_name(self):
        if self.first_name:
            if self.last_name:
                return self.first_name + ' ' + self.last_name
            else:
                return self.first_name
        else:
            return self.last_name or self.username
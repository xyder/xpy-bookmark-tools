from werkzeug.security import generate_password_hash
from wtforms import validators
from wtforms.widgets import TextInput, PasswordInput
from application import db


class CustomTextWidget(TextInput):
    def __call__(self, *args, **kwargs):
        if 'autocomplete' not in kwargs:
            kwargs['autocomplete'] = 'off'
        return super(CustomTextWidget, self).__call__(*args, **kwargs)


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

    @staticmethod
    def get_field_args_login():
        """
        Gets the field arguments for the automatic form creation.
        """

        return {
            User.username.key: {'widget': CustomTextWidget(), 'label': 'Username',
                                'validators': [validators.DataRequired()]},
            User.password.key: {'widget': PasswordInput(), 'label': 'Password',
                                'validators': [validators.DataRequired()]}
        }

    @staticmethod
    def get_field_args_create():
        """
        Gets the field arguments for the automatic form creation.
        """
        return {
            User.first_name.key: {'widget': CustomTextWidget(), 'label': 'First Name'},
            User.last_name.key: {'widget': CustomTextWidget(), 'label': 'Last Name'},
            User.username.key: {'widget': CustomTextWidget(), 'label': 'Username',
                                'validators': [validators.DataRequired()]},
            User.password.key: {'widget': PasswordInput(), 'label': 'Password',
                                'validators': [validators.DataRequired(),
                                               validators.EqualTo('confirm', message='Password must match.')]}
        }

    @property
    def get_full_name(self):
        if self.first_name:
            if self.last_name:
                return self.first_name + ' ' + self.last_name
            else:
                return self.first_name
        else:
            return self.last_name or self.username
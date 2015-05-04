from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wtforms.widgets import TextInput


class CustomTextWidget(TextInput):
    """
    Custom text widget with disabled 'autocomplete' attribute.
    """

    def __call__(self, *args, **kwargs):
        if 'autocomplete' not in kwargs:
            kwargs['autocomplete'] = 'off'
        return super(CustomTextWidget, self).__call__(*args, **kwargs)


class DBManager():
    """
    Class that creates and manages a SQLAlchemy engine and session.
    """

    def __init__(self, path, readonly=False):
        self.engine = create_engine('sqlite:///' + path)
        self.Session = sessionmaker(bind=self.engine, autoflush=(not readonly))
        self.session = self.Session()

        if readonly:
            def flush_patch(*args, **kwargs):
                del args, kwargs
                raise Exception('Database is read-only.')

            self.session._flush = flush_patch

from .access_level import AccessLevel
from .user import User

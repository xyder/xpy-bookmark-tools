from wtforms.widgets import TextInput


class CustomTextWidget(TextInput):
    def __call__(self, *args, **kwargs):
        if 'autocomplete' not in kwargs:
            kwargs['autocomplete'] = 'off'
        return super(CustomTextWidget, self).__call__(*args, **kwargs)

from .access_level import AccessLevel
from .user import User

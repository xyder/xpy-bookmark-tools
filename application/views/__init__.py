from flask import flash, session

from application.utils import Authentication


def has_flash(message, category='message'):
    """
    Checks if the flashes list contains the specified message.

    :return: True if it is present.
    """

    for f in session.get('_flashes', []):
        if f[0] == category and f[1] == message:
            return True
    return False


def flash_once(message, category='message'):
    if not has_flash(message, category):
        flash(message, category)


def check_errors():
    """
    Checks if there are any application level errors.

    :return: True if there are errors.
    """

    default_user_present_error = 'Warning: Change default login info to something ' \
                                 'unique to prevent a potential security risk.'

    # checks if the default user is present
    if Authentication.check_authorization('admin', 'password'):
        flash_once(default_user_present_error)

from . import admin_views, main_views, forms

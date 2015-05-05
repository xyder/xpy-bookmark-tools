from flask import request, redirect, url_for
import flask.ext.login as login
from flask.ext.admin import expose, BaseView
from flask.ext.admin.contrib.sqla import ModelView

from application.views import check_errors


class AdminBaseView():
    """
    Base class for admin views
    """

    @staticmethod
    def is_accessible():
        """
        Returns true if user is authenticated.
        """

        return login.current_user.is_authenticated()

    def _handle_view(self, name, **kwargs):
        """
        Pre-handler for the view. Redirects in case of inaccesibility.
        """

        # ignore arguments
        del name, kwargs

        if not self.is_accessible():
            return redirect(url_for('admin.login_view', next=request.url))
        else:
            check_errors()


class AdminView(AdminBaseView, BaseView):
    """
    Class that manages a generic admin view.
    """

    def render_template(self, template='', **kwargs):
        """
        Returns the render of the class template or the one specified.
        """

        self.template = template or self.template
        if self.template:
            return self.render(self.template, **kwargs)
        else:
            return redirect(url_for('admin.index'))

    @expose('/', methods=['GET'])
    def index(self):
        """
        Serves the index view
        """

        return self.render_template()

    def __init__(self, template=None, *args, **kwargs):
        self.template = template
        super(AdminView, self).__init__(*args, **kwargs)


class AdminModelView(AdminBaseView, ModelView):
    """
    Class that manages a generic admin model view.
    """
    pass

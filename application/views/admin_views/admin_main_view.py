from flask import request, redirect, url_for
import flask.ext.login as login
from flask.ext.admin import AdminIndexView, expose, helpers

from application.views import forms, check_errors


class AdminMainView(AdminIndexView):
    """
    Main view for the admin area.
    """

    @expose('/')
    def index(self):
        """
        Serves the index endpoint.
        """

        # prevent unauthorized access
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view', next=request.url))

        check_errors()
        return super(AdminMainView, self).index()

    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        """
        Manages the login action.
        """

        req_form = forms.LoginForm(request.form)
        if helpers.validate_form_on_submit(req_form):
            user = req_form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(request.args.get('next') or '/admin')

        check_errors()

        self._template_args['form'] = req_form
        return super(AdminMainView, self).index()

    @expose('/logout')
    def logout_view(self):
        """
        Manages the logout action.
        """

        login.logout_user()
        return redirect(request.args.get('next') or '/')

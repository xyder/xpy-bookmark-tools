from werkzeug.security import generate_password_hash

from application.views import forms
from . import AdminModelView


class AdminUserModelView(AdminModelView):
    """
    CLass that manages a User admin model view.
    """

    # set the passwords to be masked
    column_formatters = dict(password=lambda v, c, m, p: '* * * * *')

    def create_form(self, obj=None):
        """
        Set the Create form.
        """

        return forms.UserCreateForm()

    def edit_form(self, obj=None):
        """
        Set the Edit form.
        """

        return forms.UserEditForm(obj=obj)

    def create_model(self, form):
        """
        Manage the model before Create.
        """

        form.password.data = generate_password_hash(form.password.data)
        return super(AdminUserModelView, self).create_model(form)

    def update_model(self, form, model):
        """
        Manage the model before Edit.
        """

        form.password.data = generate_password_hash(form.password.data)
        return super(AdminUserModelView, self).update_model(form, model)

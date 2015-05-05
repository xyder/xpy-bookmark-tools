import os
import random
from flask import request, redirect, url_for, flash, session
from flask.ext.admin import expose, AdminIndexView, helpers, BaseView
from flask.ext.admin.contrib.sqla import ModelView
import flask.ext.login as login
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from . import forms, check_errors
from config import PathsConfig


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


class AdminFileManagerView(AdminView):
    """
    Class that manages a file manager admin view.
    """

    SELECTED = 'selected_uploaded_file'

    @staticmethod
    def get_file_path(filename=''):
        """
        Builds the path to the file from the upload folder, if it exists.

        :param filename(str): the filename to be checked.

        :return: (fname, fpath) - If fname is empty, filename was not specified.
        If fname is not empty and fpath is empty, file was not found.
        """

        if not filename:
            return '', ''
        filename = secure_filename(filename)
        file_path = os.path.join(PathsConfig.UPLOAD_FOLDER, filename)

        if os.path.isfile(file_path):
            return filename, file_path
        else:
            return filename, ''

    @staticmethod
    def is_selected(fname='', fpath=''):
        """
        Checks if the specified file is selected
        """

        sel = AdminFileManagerView.SELECTED
        return session[sel][0] == fname and session[sel][1] == fpath

    @staticmethod
    def set_selected(fname='', fpath=''):
        """
        Sets the selected file or deselects it if already selected or if deselect is specified
        """
        sif = AdminFileManagerView.SELECTED
        if sif not in session:
            session[sif] = fname, fpath
            return

        session[sif] = ('', '') if AdminFileManagerView.is_selected(fname, fpath) else (fname, fpath)

    @staticmethod
    def is_allowed(filename):
        """
        Checks if given filename is allowed.
        """

        if '.' not in filename:
            return False

        if filename in PathsConfig.ALLOWED_FILES:
            return True

        if filename.rsplit('.', 1)[1] in PathsConfig.ALLOWED_EXTENSIONS:
            return True

        return False

    @staticmethod
    def save_file(file, filename):
        """
        Saves the file to the upload folder with the specified filename, resolving name conflicts.
        """

        file_path = os.path.join(PathsConfig.UPLOAD_FOLDER, filename)

        if os.path.isfile(file_path):
            # insert a random number to make the file name unique
            filename_parts = filename.rsplit('.', 1)
            filename = filename_parts[0] + '_-_%08d.' % random.randint(0, 99999999) + filename_parts[1]

            flash('File name already exists. New name generated: "' + filename + '".')
            file_path = os.path.join(PathsConfig.UPLOAD_FOLDER, filename)

        os.makedirs(PathsConfig.UPLOAD_FOLDER, exist_ok=True)
        file.save(file_path)

    @expose('/upload', methods=['POST'])
    def upload_file(self):
        """
        Receives an upload request and saves the file to the upload folder.
        """

        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)

            if self.is_allowed(file.filename):
                self.save_file(file, filename)
                flash('File created successfully.', 'info')
            else:
                flash('File "' + file.filename + '" is not allowed.')
        else:
            flash('File parameter not received.')
        return redirect(url_for(self.endpoint + '.index'))

    @expose('/delete', methods=['POST'])
    def delete_file(self):
        """
        Receives a delete file request and deletes the file from the upload folder.
        """

        fname, fpath = self.get_file_path(request.form['filename'])
        if fname and fpath:
            os.remove(fpath)

            # deselect if selected
            if self.is_selected(fname, fpath):
                self.set_selected(fname, fpath)

            flash('File delete successfully.', 'info')
        else:
            flash('Filename parameter not received.' if not fname else 'File "' + fname + '" was not found.')
        return redirect(url_for(self.endpoint + '.index'))

    @expose('/', methods=['POST'])
    def open_file(self):
        """
        Selects and opens an uploaded file.
        """

        fname, fpath = self.get_file_path(request.form['filename'])
        if fname and fpath:
            self.set_selected(fname, fpath)
        else:
            flash('Filename parameter not received.' if not fname else 'File "' + fname + '" was not found.')
        return redirect(url_for(self.endpoint + '.index'))

    @expose('/', methods=['GET'])
    def index(self):
        """
        Serves the file manager index view.
        """

        if AdminFileManagerView.SELECTED not in session:
            self.set_selected()

        file_list = [f for f in os.listdir(PathsConfig.UPLOAD_FOLDER)
                     if os.path.isfile(os.path.join(PathsConfig.UPLOAD_FOLDER, f))]

        params = {
            'file_list': file_list,
            'selected_file': session[AdminFileManagerView.SELECTED]
        }

        return self.render_template(params=params)


class AdminModelView(AdminBaseView, ModelView):
    """
    Class that manages a generic admin model view.
    """
    pass


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

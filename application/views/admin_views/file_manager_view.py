import os
import random
from flask import session, flash, redirect, request, url_for
from flask.ext.admin import expose
from werkzeug.utils import secure_filename

from . import AdminView
from config import PathsConfig


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

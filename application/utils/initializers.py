import os
from flask import abort, send_file
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.restful import Api
from werkzeug.utils import secure_filename

from application import views, models
from config import ActiveConfig, PathsConfig


def init_db(db):
    """
    Initializes data in the database if necessary.
    """

    # will create directory if not exist
    os.makedirs(PathsConfig.DATABASES_DIR, exist_ok=True)

    # will create database and tables if not exist
    db.create_all()

    default_title = 'Administrator'
    # add the default title if missing
    if models.AccessLevel.query.filter_by(title=default_title).first() is None:
        default_level = models.AccessLevel(default_title)
        db.session.add(default_level)
        db.session.commit()

    admin_id = models.AccessLevel.query.filter_by(title=default_title).first().id

    # will create a default user if no administrator user exists
    if models.User.query.filter_by(access_level_id=admin_id).first() is None:
        default_user = models.User.query.filter_by(username='admin').first()

        if default_user is None:
            # create user 'admin' if it doesn't exist
            default_user = models.User('admin', 'password', 'John', 'Smith', admin_id)
            db.session.add(default_user)
        else:
            # change access level to default administrator level
            default_user.access_level_id = admin_id
        db.session.commit()


# initialize flask login
def init_login(app):
    """
    Initializes flask-login related objects.

    :param app: The Flask instance.
    """

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)


def init_admin(app, db):
    """
    Initializes flask-admin related objects.

    :param app: The Flask instance.

    :param db: The app database instance.
    """

    admin = Admin(app, ActiveConfig.APP_NAME, index_view=views.admin_views.AdminMainView())

    # register admin views
    admin.add_view(views.admin_views.AdminUserModelView(models.User,
                                                        db.session,
                                                        name='Users',
                                                        endpoint='users'))
    admin.add_view(views.admin_views.AdminModelView(models.AccessLevel,
                                                    db.session,
                                                    name='Access Levels',
                                                    endpoint='access-levels'))

    os.makedirs(PathsConfig.UPLOAD_FOLDER, exist_ok=True)
    admin.add_view(views.admin_views.AdminImportedFilesView(PathsConfig.UPLOAD_FOLDER,
                                                            '/imported_files/',
                                                            endpoint='imported-files',
                                                            name='Imported Files'))


def init_rest(app):
    """
    Initializes Flask-Restful related objects and server resources.

    :param app: The Flask instance.
    """

    rest_api = Api(app)
    rest_api.add_resource(views.rest_resources.ImportedResource,
                          ActiveConfig.REST_URL_IMPORTED,
                          ActiveConfig.REST_URL_IMPORTED_FILE,
                          ActiveConfig.REST_URL_IMPORTED_ITEM,
                          ActiveConfig.REST_URL_IMPORTED_ITEM_ATTR)


def send_imported_file(filename):
    """
    View function that sends files from the upload directory.

    :param filename: name of the file to be sent.

    :return: the server response.
    """
    filename = secure_filename(filename)
    file_path = os.path.join(PathsConfig.UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        abort(404)


def init_app(app):
    """
    Initializes the Flask application objects and registers the views.

    :param app: The Flask instance.
    """

    app.add_url_rule('/', endpoint='index', view_func=views.main_views.IndexView.as_view('index'))
    app.add_url_rule('/imported_files/<filename>', endpoint='imported_files', view_func=send_imported_file)

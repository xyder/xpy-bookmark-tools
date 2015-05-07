import os


class PathsConfig(object):
    """
    Class containing path constants
    """
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR = os.path.join(BASE_DIR, 'application')
    STATIC_DIR = os.path.join(APP_DIR, 'static')
    DATABASES_DIR = os.path.join(BASE_DIR, 'databases')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'imported_files')
    ALLOWED_FILES = ['places.sqlite']
    ALLOWED_EXTENSIONS = ['html']

    @staticmethod
    def get_db_path(file, db_dir=DATABASES_DIR):
        return 'sqlite:///' + os.path.join(db_dir, file)


class AppConfig(object):
    """
    Class containing base application constants
    """
    SERVER_PORT = 5000
    SERVER_HOST = "127.0.0.1:"
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = PathsConfig.get_db_path('data.sqlite')

    WTF_CSRF_ENABLED = False
    SECRET_KEY = "this is a secret key"

    REST_URL_BASE = '/api/v1.0'
    REST_URL_IMPORTED = REST_URL_BASE + '/imported'
    REST_URL_IMPORTED_FILE = REST_URL_IMPORTED + '/<file_name>'
    REST_URL_IMPORTED_ITEM = REST_URL_IMPORTED_FILE + '/<item_id>'
    REST_URL_IMPORTED_ITEM_ATTR = REST_URL_IMPORTED_ITEM + '/<attr>'

    APP_NAME = 'XPy Bookmark Tools'


class DevConfig(AppConfig):
    """
    Class containing development environment constants
    """
    SERVER_PORT = 3000
    DEBUG = True


class ProductionConfig(AppConfig):
    """
    Class containing production environment constants
    """
    SERVER_PORT = 80


class GenericConfig(DevConfig):
    """
    Class base for the active configuration. Change inheritance to quickly change application
    configurations.
    """
    pass


class TestingConfig(DevConfig):
    """
    Class containing constants for automatic testing.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = PathsConfig.get_db_path('test.sqlite')


class ActiveConfig(GenericConfig):
    """
    Class containing the active configuration constants. Should not be changed
    """
    SERVER_NAME = GenericConfig.SERVER_HOST + str(GenericConfig.SERVER_PORT)

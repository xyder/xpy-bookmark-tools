import os


class PathsConfig(object):
    """
    Class containing path constants
    """
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    APP_DIR = os.path.join(BASE_DIR, 'application')
    STATIC_DIR = os.path.join(APP_DIR, 'static')


class AppConfig(object):
    """
    Class containing base application constants
    """
    SERVER_PORT = 5000
    SERVER_HOST = "127.0.0.1:"
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PathsConfig.BASE_DIR, 'data.sqlite')

    APP_NAME = 'XPy Bookmark Tools'


class TestingConfig(AppConfig):
    """
    Class containing testing environment constants
    """
    SERVER_PORT = 3000
    DEBUG = True


class ProductionConfig(AppConfig):
    """
    Class containing production environment constants
    """
    SERVER_PORT = 80


# class renaming to quickly switch between configurations
class GenericConfig(TestingConfig):
    """
    Class used as a buffer between the testing and the production classes for
    easy switching between the two
    """
    pass


class ActiveConfig(GenericConfig):
    """
    Class containing the active configuration constants. Should not be changed
    """
    SERVER_NAME = GenericConfig.SERVER_HOST + str(GenericConfig.SERVER_PORT)

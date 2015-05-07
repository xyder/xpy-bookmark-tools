from flask.ext.restful import Resource
from application.utils import Authentication


class ImportedResource(Resource):
    """
    Class that processes data fetching from imported files.
    """

    @Authentication.login_required
    def get(self, file_name='', item_id='', attr=''):
        pass

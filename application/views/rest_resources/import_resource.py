from flask.ext.restful import Resource, abort
from application.utils import Authentication


class ImportedResource(Resource):
    """
    Class that processes data fetching from imported files.
    """

    @Authentication.login_required
    def get(self, file_name='', item_id='', attr=''):
        if not file_name:
            # file list is requested
                return {'files': 'files'}

        if not item_id:
            # root items are requested
                return {'root_items': 'root items'}

        if not attr:
            # item object is requested
                return {'item': 'item'}

        if attr == 'children':
            # item children are requested
                return {'children': 'children'}

        # bad request
        abort(400, message='Request could not be satisfied.')

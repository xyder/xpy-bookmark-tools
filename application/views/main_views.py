from flask import render_template
from flask.views import View


class IndexView(View):
    methods = ['GET']

    def __init__(self, template_name='index.html', view_title='Index'):
        self.params = {
            'template_name': template_name,
            'params': {
                'title': view_title
            }
        }

    def render_template(self, context):
        return render_template(self.params['template_name'], **context)

    def dispatch_request(self):
        return self.render_template(self.params)
from application import db


class AccessLevel(db.Model):
    __tablename__ = 'access_level'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True)

    def __init__(self, title=''):
        self.title = title or ''

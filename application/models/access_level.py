from application import db


class AccessLevel(db.Model):
    __tablename__ = 'access_level'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True)
    users = db.relationship('User', backref='access_level', lazy='dynamic')

    def __init__(self, title=''):
        self.title = title or ''

    def __repr__(self):
        return self.title

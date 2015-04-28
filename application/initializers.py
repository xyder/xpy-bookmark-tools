from application.models import User, AccessLevel


def init_db(db):
    """
    Initializes data in the database if necessary.
    """

    # will create database and tables if not exist
    db.create_all()

    default_title = 'Administrator'
    if AccessLevel.query.filter_by(title=default_title).first() is None:
        default_level = AccessLevel(default_title)
        db.session.add(default_level)
        db.session.commit()

    admin_id = AccessLevel.query.filter_by(title=default_title).first().id

    # will append a default user if no administrator user exists
    if User.query.filter_by(access_level_id=admin_id).first() is None:
        default_user = User.query.filter_by(username='admin').first()

        if default_user is None:
            default_user = User('admin', 'password', 'John', 'Smith', admin_id)
            db.session.add(default_user)
        else:
            default_user.access_level_id = admin_id
        db.session.commit()
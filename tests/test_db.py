import unittest
from werkzeug.security import check_password_hash

from application.utils.initializers import init_db
from config import TestingConfig

from application import db, app, models


class DatabaseTests(unittest.TestCase):
    """
    Class for database related tests.
    """

    def setUp(self):
        """
        Set the Test Unit up
        """

        app.config.from_object(TestingConfig)
        db.session.close()

    def test_init_db(self):
        """
        Test the init_db initializer.
        """

        # TEST CASE:
        # cond:
        #   - no previous data
        # post:
        #   - default tables are generated
        #   - default access level is generated
        #   - default user is generated

        db.drop_all()
        init_db(db)

        assert db.engine.dialect.has_table(db.engine.connect(), 'users')
        assert db.engine.dialect.has_table(db.engine.connect(), 'access_level')

        default_access_level = models.AccessLevel.query.first()
        assert default_access_level is not None
        assert default_access_level.title == 'Administrator'

        default_user = models.User.query.first()
        assert default_user is not None
        assert default_user in default_access_level.users

        # TEST CASE:
        # cond:
        #   - administrator user already exists
        # post:
        #   - no change

        models.User.query.delete()

        test_user = models.User(username='test', password='test', access_level_id=default_access_level.id)
        db.session.add(test_user)
        db.session.commit()

        init_db(db)
        assert default_access_level.users.count() is 1
        assert default_access_level.users.first().username != default_user.username

        # TEST CASE
        # cond:
        #   - default user already exists
        #   - no administrator user present
        # post:
        #   - default user has administrator access

        models.User.query.delete()

        # new user will have no access level assigned at creation
        test_user = models.User(username=default_user.username, password=default_user.password)
        db.session.add(test_user)
        db.session.commit()

        assert models.User.query.get(test_user.id) not in default_access_level.users
        init_db(db)
        assert models.User.query.get(test_user.id) in default_access_level.users

        # TEST CASE:
        # cond:
        #   - only non-administrator users present
        # post:
        #   - default user is generated

        models.User.query.delete()

        # create a non-administrator user
        test_user = models.User(username='test', password='test')
        db.session.add(test_user)
        db.session.commit()

        init_db(db)
        new_default_user = default_access_level.users.first()
        assert models.User.query.count() is 2
        assert default_access_level.users.first() is not None
        assert default_user.username == new_default_user.username
        assert check_password_hash(new_default_user.password, 'password')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
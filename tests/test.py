import unittest
from tests.main import db
from tests.schema import Permission, Role, User


class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

        self.pr = Permission(name='posts:r')
        self.pw = Permission(name='posts:w')
        self.role = Role(name='Moderator', permissions=[self.pr, self.pw])
        self.user = User(username='yarbshk', password='x', role=self.role)

import unittest
from tests.main import db
from tests.schema import Permission, Role, User


def get_dict_depth(d, level=1):
    """
    Note: the method returns 2 for 1 level depth dict.
    https://stackoverflow.com/questions/23499017
    """
    if not isinstance(d, dict) or not d:
        return level
    return max(get_dict_depth(d[k], level + 1) for k in d)


class TestCase(unittest.TestCase):
    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

        self.pr = Permission(name='posts:r')
        self.pw = Permission(name='posts:w')
        self.role = Role(name='Moderator', permissions=[self.pr, self.pw])
        user = User(username='yarbshk', password='x', role=self.role)
        db.session.add(user)
        db.session.commit()
        self.user = db.session.query(User).first()

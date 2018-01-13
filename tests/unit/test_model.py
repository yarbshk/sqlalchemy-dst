import types
from tests.schema import User
from tests.test import TestCase


class ModelTest(TestCase):
    def test_as_dict(self):
        user_dict = self.user.as_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertDictEqual(user_dict, {
            'id': 1,
            'username': 'yarbshk',
            'password': 'x',
            '_secret': 'x',
            'role': None,
            'role_id': 1
        })

    def test_from_dict(self):
        user_dict = self.user.as_dict()
        user_row = User.from_dict(user_dict)
        self.assertIsInstance(user_row, User)
        self.assertEqual(user_row.username, self.user.username)
        self.assertEqual(user_row.password, self.user.password)

    def test_iter(self):
        iterator = getattr(self.user, '__iter__')()
        self.assertIsInstance(iterator, types.GeneratorType)

from sqlalchemy_dst import row2dict
from tests.test import TestCase, get_dict_depth


class Row2DictTest(TestCase):
    def test_default(self):
        user_dict = row2dict(self.user)
        self.assertIsInstance(user_dict, dict)
        self.assertDictEqual(user_dict, {
            'id': 1,
            'username': 'yarbshk',
            'password': 'x',
            '_secret': 'x',
            'role': None,
            'role_id': 1
        })

    def test_depth(self):
        user_dict1 = row2dict(self.user)
        self.assertEqual(get_dict_depth(user_dict1) - 1, 1) # force -1
        user_dict2 = row2dict(self.user, depth=3)
        self.assertEqual(get_dict_depth(user_dict2), 3)

    def test_exclude(self):
        user_dict = row2dict(self.user, depth=3, exclude={'username'})
        self.assertNotIn('username', user_dict)
        self.assertNotIn('users', user_dict['role'])
        for permission in user_dict['role']['permissions']:
            self.assertNotIn('roles', permission)

    def test_exclude_pk(self):
        # in
        user_dict1 = row2dict(self.user)
        self.assertIn('role_id', user_dict1)
        # not in
        user_dict2 = row2dict(self.user, exclude_pk=True)
        self.assertNotIn('role_id', user_dict2)

    def test_exclude_underscore(self):
        # in
        user_dict1 = row2dict(self.user)
        self.assertIn('_secret', user_dict1)
        # not in
        user_dict2 = row2dict(self.user, exclude_underscore=True)
        self.assertNotIn('_secret', user_dict2)

    def test_only(self):
        user_dict = row2dict(self.user, depth=3, only={'id', 'username'})
        self.assertDictEqual(user_dict, {
            'id': self.user.id,
            'username': self.user.username
        })

    def test_empty(self):
        with self.assertRaises(AttributeError):
            row2dict(None)

from sqlalchemy_dst import dict2row, row2dict
from tests.schema import Permission, Role, User
from tests.test import TestCase


class Dict2RowTest(TestCase):
    @property
    def user_dict(self):
        return row2dict(self.user, depth=3)

    def test_default(self):
        user_row = dict2row(self.user_dict, User)
        self.assertIsInstance(user_row, User)
        self.assertEqual(user_row.username, self.user.username)
        self.assertEqual(user_row.password, self.user.password)

    def test_rel(self):
        user_row = dict2row(self.user_dict, User, rel={
            'role': Role,
            'permissions': Permission
        })
        self.assertEqual(len(user_row.role.permissions),
                         len(self.user.role.permissions))

    def test_exclude(self):
        # in
        user_row1 = dict2row(self.user_dict, User)
        self.assertIsNotNone(user_row1.username)
        # not in
        user_row2 = dict2row(self.user_dict, User, exclude={'username'})
        self.assertIsNone(user_row2.username)

    def test_exclude_pk(self):
        # in
        user_row1 = dict2row(self.user_dict, User)
        self.assertIsNotNone(user_row1.role_id)
        # not in
        user_row2 = dict2row(self.user_dict, User, exclude_pk=True)
        self.assertIsNone(user_row2.role_id)

    def test_exclude_underscore(self):
        # in
        user_row1 = dict2row(self.user_dict, User)
        self.assertIsNotNone(user_row1._secret)
        # not in
        user_row2 = dict2row(self.user_dict, User, exclude={'password'},
                             exclude_underscore=True)
        self.assertIsNone(user_row2._secret)

    def test_only(self):
        user_row = dict2row(self.user_dict, User, rel={'role': Role},
                            only={'id', 'role'})
        self.assertEqual(user_row.id, self.user_dict['id'])
        self.assertIsNone(user_row.username)
        self.assertIsNone(user_row.password)
        self.assertIsNotNone(user_row.role)

    def test_fk_suffix(self):
        user_row = dict2row(self.user_dict, User, rel={'role': Role},
                            fk_suffix='x')
        self.assertTrue(hasattr(user_row, 'rolex'))

    def test_empty(self):
        with self.assertRaises(AttributeError):
            dict2row(self.user_dict, object)
        with self.assertRaises(TypeError):
            dict2row([], User)

import unittest
from tests.main import db


class Dict2RowTest(unittest.TestCase):
    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

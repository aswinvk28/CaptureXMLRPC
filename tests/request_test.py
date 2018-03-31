import unittest
from . import database
from . import session
from . import request

class Request_TestCase(unittest.TestCase):
    def setUp(self):
        self.fixtures = {'project_code': 'xxx123', 'unit_code': 'uuu_123', 'password': '123'}
        self.db = database.Database(db_file='sqlite_test/application.db')
        self.request = request.Request(self.db)

    def test_list_focal_point_metrics(self):
        session_id = self.db.get_session(self.fixtures['project_code'], self.fixtures['unit_code'])
        # session_id = self.db.issue_session(self.fixtures['project_code'], self.fixtures['unit_code'], "123")
        metrics = self.request.listMetrics(session_id, "all")
        self.assertIsNotNone(metrics, "The metrics array is None")
        self.assertTrue(len(metrics) > 0, "The metrics list has atleast 1 object")
        metrics = self.request.listMetrics(session_id, "circulation")
        self.assertIsNotNone(metrics, "The metrics array is None")

    def test_list_focal_point(self):
        session_id = self.db.get_session(self.fixtures['project_code'], self.fixtures['unit_code'])
        result = self.request.listFocalPoints(session_id)
        self.assertIsNotNone(result, "The result array is None")
        self.assertTrue(len(result) > 0, "The result list has atleast 1 object")


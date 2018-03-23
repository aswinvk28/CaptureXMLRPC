# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest
from . import database
from . import session

class Database_TestCase(unittest.TestCase):
    def setUp(self):
        self.fixtures = {'project_code': 'xxx123', 'unit_code': 'uuu_123', 'password': '123'}
        self.db_conn = database.Database(db_file='sqlite_test/application.db')

    def test_database_create_project(self):
        self.assertIsNotNone(self.db_conn, "The connection object is null")
        result = self.db_conn.create_project(self.fixtures['project_code'], self.fixtures['unit_code'], self.fixtures['password'])
        self.assertEqual(result, 1, "The result value is incorrect")

    def test_database_session(self):
        session_id = session.build_short_code(self.fixtures['project_code'], self.fixtures['unit_code'])
        result = self.db_conn.issue_session(self.fixtures['project_code'], self.fixtures['unit_code'], session_id)
        self.assertEqual(result, session_id, "The result value is not returning the session id")
        self.session_id = session_id

    def test_database_verify(self):
        cursor = self.db_conn.get_conn().cursor()
        cursor.execute("""
        SELECT session_id FROM session WHERE project_code = '{project_code}' AND unit_code = '{unit_code}'
        """.format(project_code=self.fixtures['project_code'], unit_code=self.fixtures['unit_code']))
        session_id = cursor.fetchone()
        if len(session_id) >= 1:
            session_id = session_id[0]
        cursor.close()
        result = self.db_conn.verify_project(self.fixtures['project_code'], self.fixtures['unit_code'], self.fixtures['password'], session_id)
        self.assertIsNotNone(result, "The project and session have not been verified")
        self.assertTrue(result, "The project and the session have been verified")

if __name__ == '__main__':
    unittest.main()

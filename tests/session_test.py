# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest
import sqlite3
from time import time
from . import database
from . import session

class Session_TestCase(unittest.TestCase):
    def setUp(self):
        self.db_conn = database.Database(db_file='sqlite_test/application.db')
        self.db = self.db_conn.get_conn()
        self.session = session.Session(self.db_conn)
        self.fixtures = {'project_code': 'xxx124', 'unit_code': 'uuu_124', 'password': '124'}
    
    def test_project_create(self):
        result = self.session.createProjectShortCode(self.fixtures['project_code'], self.fixtures['unit_code'], self.fixtures['password'])
        self.assertTrue(result, "The creation of project from session did not work, XMLRPC is a failure")

    def test_session_obtain(self):
        session_id2 = self.session.obtainSession(True, self.fixtures['project_code'], self.fixtures['unit_code'])
        self.assertIsNotNone(session_id2, "The session id " + session_id2.__str__() + " obtained is None")
        session_id = self.session.obtainSession(False, self.fixtures['project_code'], self.fixtures['unit_code'], time(), session_id2)
        self.assertEqual(session_id, session_id2, "The session ids obtained by both processes, " + session_id.__str__() + ": " + session_id2.__str__() + " are not equal")
        self.session_id = session_id

    def test_session_expire(self):
        cursor = self.db.cursor()
        cursor.execute("""
        SELECT session_id FROM session WHERE project_code = '{project_code}' AND unit_code = '{unit_code}'
        """.format(project_code=self.fixtures['project_code'], unit_code=self.fixtures['unit_code']))
        session_id = cursor.fetchone()
        if len(session_id) > 0:
            session_id = session_id[0]
        result = self.session.expireSession(session_id)
        self.assertTrue(result, "The expiring of session did not work, XMLRPC is a failure")

    def test_project_verify(self):
        result = self.session.verifyProjectShortCode(self.fixtures['project_code'], self.fixtures['unit_code'], self.fixtures['password'], "")
        self.assertIsNone(result, "The project and session have not been verified")
        self.assertTrue(result, "The project and the session have been verified")

if __name__ == '__main__':
    unittest.main()


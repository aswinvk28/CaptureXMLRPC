import sqlite3
from datetime import datetime
import time
import hashlib
from .rpc_helpers import Fault

class Database(object):

    def __init__(self, db_file='sqlite/application.db'):
        self.conn = sqlite3.connect(db_file)

    def get_cursor(self, cursor):
        cursor.close()
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def get_conn(self):
        return self.conn

    def delete_session(self, project_code, unit_code):
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM session WHERE project_code = '{project_code}' AND
        unit_code = '{unit_code}'
        """.format(project_code=project_code, unit_code=unit_code))
        self.conn.commit()
        result = cursor.rowcount
        cursor.close()
        return result
    
    def expire_session(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM session WHERE session_id = '{session_id}'
        """.format(session_id=session_id))
        self.conn.commit()
        result = cursor.rowcount
        cursor.close()
        return result

    def create_project(self, project_code, unit_code, password):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM project WHERE project_code = '{project_code}' AND unit_code = '{unit_code}'
        """.format(project_code=project_code, unit_code=unit_code))
        if cursor.rowcount == 1:
            cursor.close()
            raise Fault('project_exists', 'A project with the same combination of Project Code and Unit Code exists')
        cursor = self.get_cursor(cursor)
        hash = hashlib.md5()
        hash.update(password.encode())
        password = hash.hexdigest()
        cursor.execute("""
        INSERT INTO project (project_code, unit_code, password)
        VALUES ('{project_code}', '{unit_code}', '{password}')
        """.format(project_code=project_code, unit_code=unit_code, password=password))
        self.conn.commit()
        result = cursor.rowcount
        if cursor.rowcount != 1:
            raise Fault('sql_error')
        cursor.close()
        return result
    
    # status = 'issued', 'registered', 'expired'
    # expiry in seconds
    def issue_session(self, project_code, unit_code, session_id):
        try:
            cursor = self.conn.cursor()
            result = self.expire_session(session_id)
            if result:
                raise Exception('session_duplicate')
            status = 'issued'
            cursor.execute("""
            INSERT INTO session (project_code, unit_code, session_id, 
            status, expiry) VALUES 
            ('{project_code}', '{unit_code}', '{session_id}', '{status}', '{expiry}')
            """.format(
                project_code=project_code, unit_code=unit_code,
                session_id=session_id, status=status,
                expiry=time.time() + 604800))
            self.conn.commit()
            result = cursor.rowcount
            cursor.close()
            if result:
                return session_id
            elif result == -1:
                raise Exception('session_disallowed')
        except Exception as exception:
            raise Exception(exception.args[0])
        return None

    def verify_session(self, session_id):
        cursor = self.conn.cursor()
        timestamp = time.time()
        cursor.execute("""
        SELECT * FROM session WHERE session_id = '{session_id}'
        """.format(session_id=session_id))

        session = cursor.fetchone()
        cursor.close()
        if session and len(session) > 0 and session[4] > timestamp:
            return True
        else:
            self.expire_session(session_id)
            raise Fault('session_expired', "Session has been expired")
        return False
    
    def verify_project(self, project_code, unit_code, password, session_id):
        cursor = self.conn.cursor()
        hash = hashlib.md5()
        hash.update(password.encode())
        password = hash.hexdigest()
        cursor.execute("""
        SELECT COUNT(*) FROM project WHERE project_code = '{project_code}' AND unit_code = '{unit_code}'
        AND password = '{password}'
        """.format(project_code=project_code, unit_code=unit_code, password=password))
        result = cursor.fetchone()
        if len(result) > 0:
            result = result[0]
        cursor.close()
        if result == 0 or result == -1:
            raise Fault('verification_failure', "verification failure")
        try:
            result = self.verify_session(session_id)
            return result
        except Exception as e:
            raise e
        return False

    # database helper class
    def get_session(self, project_code, unit_code):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT session_id FROM session WHERE project_code = '{project_code}' AND unit_code = '{unit_code}'
        """.format(project_code=project_code, unit_code=unit_code))
        session_id = cursor.fetchone()
        cursor.close()
        return session_id[0]

    def get_suite(self):
        pass

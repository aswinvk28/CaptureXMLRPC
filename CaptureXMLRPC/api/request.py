from .. import database
from datetime import datetime
from ..rpc_helpers import Fault
from ..rpc_helpers import get_code
import base64
import random

class Request():

    def __init__(self):
        self.database = database.Database()
        self.db = self.database.get_conn()
        
    def listMetrics(self, session_id, filter):
        result = self.database.verify_session(session_id)
        if not result:
            raise Fault('session_error', "An error occurred in verifying the session")
        cursor = self.db.cursor()
        cursor.execute("""
        SELECT name FROM focal_point_metrics
        """)
        metrics = cursor.fetchall()
        if len(metrics) == 0:
            cursor.close()
            raise Fault('data_nonexistent')
        result = list()
        for metric in metrics:
            result.append(metric)
        cursor.close()
        return result
            
    # def listFocalPoints(self, session_id, client):
    #     result = self.database.verify_session(session_id)
    #     if not result:
    #         raise Fault('session_error', "An error occurred in verifying the session")
    #     (project_code, unit_code) = get_code(client.App)
        
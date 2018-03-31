from .. import database
from datetime import datetime
from ..rpc_helpers import Fault
from ..rpc_helpers import get_code
import base64
import random

class Request():

    def __init__(self, database):
        self.database = database
        self.db = self.database.get_conn()
        
    def listMetrics(self, session_id, filter=None):
        result = self.database.verify_session(session_id)
        if not result:
            raise Fault('session_error', "An error occurred in verifying the session")
        cursor = self.db.cursor()
        if filter != 'all':
            filter_string = " WHERE type = '" + filter + "'"
        else:
            filter_string = ""
        cursor.execute("""
        SELECT name, type FROM focal_point_metrics
        """ + filter_string.__str__() + " ORDER BY type ASC")
        metrics = cursor.fetchall()
        if len(metrics) == 0:
            cursor.close()
            raise Fault('data_nonexistent')
        result = list()
        if filter != "all":
            for metric in metrics:
                result.append(metric[0])
        else:
            values = dict()
            for metric in metrics:
                values[metric[1]] = metric[0]
            result = values
        cursor.close()
        return result

    def listFocalPoints(self, session_id, app=None):
        filter_string = ""
        suite = None
        database = self.database
        if app:
            length = app.Length
            suite = app.App
            filter_string += " LIMIT 0," + length
        if suite:
            database = self.database.get_suite(suite)
        result = database.verify_session(session_id)
        if not result:
            raise Fault('session_error', "An error occurred in verifying the session")
        cursor = self.db.cursor()
        cursor.execute("""
        SELECT name FROM suite_focal_point
        """ + filter_string.__str__())
        values = cursor.fetchall()
        if len(values) == 0:
            cursor.close()
            raise Fault('data_nonexistent')
        result = list()
        for name in values:
            result.append(name[0])
        return result
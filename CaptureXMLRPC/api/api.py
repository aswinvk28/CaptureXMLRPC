from .. import database
from datetime import datetime
from ..rpc_helpers import Fault
from ..rpc_helpers import get_code
import base64
import random
from .request import Request
from ..base.session import Session

class Api(Session, Request):

    def __init__(self, database):
        self.database = database
        self.db = self.database.get_conn()


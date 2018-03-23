from flask import Flask
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from .database import Database
from . import session
from . import request

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/XmlRpcService')

server = SimpleXMLRPCServer(('127.0.0.1', 8000), requestHandler=RequestHandler)

server.register_instance(session.Session())
server.register_instance(request.Request())

server.serve_forever()
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from . import database
from .api import api

PORT = 8080
HOST = '192.168.56.102'

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/XmlRpcService')

server = SimpleXMLRPCServer((HOST, PORT), requestHandler=RequestHandler)
server.register_introspection_functions()

db = database.Database(db_file='sqlite_test/application.db')
server.register_instance(api.Api(database=db))

print("The server is running at Port: " + PORT.__str__() + 
", Host: " + HOST.__str__())

server.serve_forever()
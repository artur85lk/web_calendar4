# from flask import Flask
# import sys
# from flask_restful import Resource, Api, marshal_with, fields
#
# app = Flask('main')
# api = Api(app)
#
# class TodoDao(object):
#     def __init__(self, task, description):
#         self.task = task
#         self.description = description
#
# resource_fields = {
#     'task':   fields.String,
#     'description':    fields.String
# }
#
# class Todo(Resource):
#     @marshal_with(resource_fields)
#     def get(self, **kwargs):
#         return TodoDao(task=20072017, description="I can't feel you there")
#
#
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         arg_host, arg_port = sys.argv[1].split(':')
#         app.run(host=arg_host, port=arg_port)
#     else:
#         app.run(host="localhost", port=8000, debug=True)

from flask import Flask
from flask_restful import Resource, Api, reqparse
from marshmallow import Schema, fields


app = Flask('main')
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('severity')

class TaskSchema(Schema):
    name = fields.String()
    description = fields.String()
    severity = fields.Integer()

class TaskResource(Resource):
    def get(self):
        schema = TaskSchema()
        args = parser.parse_args()
        return schema.dump(args)

api.add_resource(TaskResource, '/')

app.run(host="localhost", port=8000, debug=True)



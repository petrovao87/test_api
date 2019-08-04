from flask import Flask, jsonify, request
from sqlalchemy import update, exc
import requests
from flask_restful import reqparse, abort, Api, Resource
from db import db_session, Process, ProcessPerformer, ProcessParameter, ProcessQuota, ProcessStartCondition

from requests import put, get

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


def abort_if_process_doesnt_exist(process_id, processes):
    # return processes
    if process_id not in processes:
        abort(404, message="process {} doesn't exist".format(process_id))


parser = reqparse.RequestParser()

# parser.add_argument('task')
# parser.add_argument('todo_id')

# Process table
parser.add_argument('process_id')# process_id
parser.add_argument('process_name')
parser.add_argument('process_description')
parser.add_argument('activity_flag')
parser.add_argument('process_performer_id')
#
# # ProcessParameter table
parser.add_argument('parameter_name')
parser.add_argument('parameter_value')
# # parser.add_argument('process_id') #####
#
# # ProcessStartCondition table
parser.add_argument('condition_type')
parser.add_argument('condition_value')
# # parser.add_argument('process_id') #####
#
# # ProcessPerformer table
# # parser.add_argument('process_performer_id') ####
parser.add_argument('performer_name')
parser.add_argument('performer_description')
#
# # ProcessQuota
parser.add_argument('quota_type')
parser.add_argument('quota_value')
# # parser.add_argument('process_id') #####







# Todo
# shows a single todo item and lets you delete a todo item
class Processes(Resource):
    def get(self, process_id):
        # abort_if_todo_doesnt_exist(todo_id)
        # return TODOS[todo_id]
        # print(process_id)
        ids = 0
        result = {}
        # user_query = db_session.query(Process).join(ProcessPerformer).filter(Process.process_id == process_id).first()
        # # print(user_query)
        # result['process_id ' + str(user_query.process_id)] = {'process_name': user_query.process_name,
        #                                                          'description': user_query.process_description,
        #                                                          'activity_flag': user_query.activity_flag,
        #                                                          'process_performer':
        #                                                              {'process_performer_id': user_query.process_performer_id,
        #                                                               'name': user_query.process_performer.performer_name,
        #                                                               'description': user_query.process_performer.performer_description}}


        user_query = db_session.query(Process).join(ProcessParameter). \
            filter(Process.id == process_id)
        user_query = user_query.join(ProcessStartCondition). \
            filter(Process.id == process_id)
        user_query = user_query.join(ProcessPerformer). \
            filter(Process.process_id == process_id)
        user_query = user_query.join(ProcessQuota). \
            filter(Process.id == process_id).first()

        if user_query is not None:
            result['process_id ' + str(user_query.process_id)] = \
                {'process_id': user_query.process_id,
                 'process_name': user_query.process_name,
                 'description': user_query.process_description,
                 'activity_flag': user_query.activity_flag,
                 'process_parameter':
                     {'parameter_name': user_query.process_parameter[0].parameter_name,
                      'parameter_value': user_query.process_parameter[0].parameter_value},
                 'process_start_condition':
                     {'condition_type': user_query.process_start_condition[0].condition_type,
                      'condition_value': user_query.process_start_condition[0].condition_value},
                 'process_performer':
                     {'process_performer_id': user_query.process_performer.process_performer_id,
                      'name': user_query.process_performer.performer_name,
                      'description': user_query.process_performer.performer_description},
                 'process_quota':
                     {'quota_type': user_query.process_quota[0].quota_type,
                      'quota_value': user_query.process_quota[0].quota_value}}
            return result
        else:
            return abort(404, message="process {} doesn't exist".format(process_id))

    # def delete(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '', 204
class ProcessesUpdate(Resource):
    def put(self, process_id):
        args = parser.parse_args()
        # user_query = db_session.query(Process).join(ProcessPerformer).filter(Process.process_id == process_id)
        # db_session.query(Process, ProcessPerformer).filter(Process.process_id == process_id).update(a)
        # db_session.query(Process).filter(Process.process_id == process_id).update(args)
        # task = {'task': args['task']}
        # coin = Process(request.form['data'])
        # db_session.add(coin)
        # db_session.commit()
        # print(coin)
        # db_session.add(coin)
        # db_session.commit()
        dict_to_update = {}
        print(locals())
        for i in args:
            print(i)
            if args[i] is not None:
                dict_to_update[i] = args[i]
        print(dict_to_update)
        db_session.query(Process).filter(Process.process_id == process_id).update(dict_to_update)
        # process.update().values(a).where(Process.process_id == process_id)
        db_session.commit()
        for i in dict_to_update:
            print(i)
            # print(dir(user_query))
            # print(locals())
            # print(args[i])
            # user_query[i] = args[i]
            # print(user_query.i)
        # db_session.commit()

        return dict_to_update, 201
        # TODOS[todo_id] = task
        # return task, 201
        # print(user_query)
        # abort_if_process_doesnt_exist(process_id, user_query)

class ProcessesParameterUpdate(Resource):
    def put(self, process_id):
        args = parser.parse_args()
        dict_to_update = {}
        for i in args:
            if args[i] is not None:
                dict_to_update[i] = args[i]
        user_query = db_session.query(ProcessParameter).filter(ProcessParameter.process_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(404, message="process {} has not this argument".format(process_id))
        for i in dict_to_update:
            print(i)
        result = {}
        user_query = user_query.first()
        if user_query is not None:
            db_session.commit()
            result['process_id ' + str(user_query.process_id)] = \
                {'process_parameter':
                     {'parameter_name': user_query.parameter_name,
                      'parameter_value': user_query.parameter_value}
                 }
            return result, 201
        else:
            return abort(404, message="process {} doesn't exist".format(process_id))


class ProcessesStartConditionUpdate(Resource):
    def put(self, process_id):
        args = parser.parse_args()
        dict_to_update = {}
        for i in args:
            if args[i] is not None:
                dict_to_update[i] = args[i]
        user_query = db_session.query(ProcessStartCondition).filter(ProcessStartCondition.process_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(404, message="process {} has not this argument".format(process_id))
        for i in dict_to_update:
            print(i)
        result = {}
        user_query = user_query.first()
        if user_query is not None:
            db_session.commit()
            result['process_id ' + str(user_query.process_id)] = \
                {'process_start_condition':
                    {'condition_type': user_query.condition_type,
                     'condition_value': user_query.condition_value}
                 }
            return result, 201
        else:
            return abort(404, message="process {} doesn't exist".format(process_id))


# TodoList
# shows a list of all todos, and lets you POST to add new tasks


class ProcessesList(Resource):
    def get(self):
        # return TODOS
        result = {}
        # user_query = db_session.query(Process).join(ProcessPerformer).\
        #     filter(Process.process_performer_id == ProcessPerformer.id).all()
        # print(user_query[0].process_performer.performer_name)

        user_query = db_session.query(Process).join(ProcessParameter). \
            filter(Process.id == ProcessParameter.process_id)
        user_query = user_query.join(ProcessStartCondition). \
            filter(Process.id == ProcessStartCondition.process_id)
        user_query = user_query.join(ProcessPerformer). \
            filter(Process.process_performer_id == ProcessPerformer.id)
        user_query = user_query.join(ProcessQuota). \
            filter(Process.id == ProcessQuota.process_id).all()


        print(user_query[0].process_start_condition[0].condition_type,
              user_query[0].process_parameter[0].parameter_name,
              user_query[0].process_quota[0].quota_value)

        for i in range(len(user_query)):
            result['process_id ' + str(user_query[i].process_id)] = \
                {'process_id': user_query[i].process_id,
                 'process_name': user_query[i].process_name,
                 'description': user_query[i].process_description,
                 'activity_flag': user_query[i].activity_flag,
                 'process_parameter':
                     {'parameter_name': user_query[i].process_parameter[0].parameter_name,
                      'parameter_value':  user_query[i].process_parameter[0].parameter_value},
                 'process_start_condition':
                     {'condition_type': user_query[i].process_start_condition[0].condition_type,
                      'condition_value': user_query[i].process_start_condition[0].condition_value},
                 'process_performer':
                     {'process_performer_id': user_query[i].process_performer.process_performer_id,
                      'name': user_query[i].process_performer.performer_name,
                      'description': user_query[i].process_performer.performer_description},
                 'process_quota':
                     {'quota_type': user_query[i].process_quota[0].quota_type,
                      'quota_value': user_query[i].process_quota[0].quota_value}}
        return result


    def post(self):
        args = parser.parse_args()
        # print(args)
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = 'todo%i' % todo_id
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201
        # print(args['process_id'])
        # a = args.task
        # b = args.process_id
        # return args.task, 201
        # user_query = db_session.query(Process).join(ProcessPerformer).\
                # filter(Process.process_id == process_id).first()
        # user_query.activity_flag =
        # print(args['todo_id'], args['task'])
        user_query = db_session.query(ProcessPerformer).filter(ProcessPerformer.process_performer_id == args.process_performer_id).first()
        process = Process(process_id=args.process_id, process_name=args.process_name, process_description='description', activity_flag='flag', process_performer_id=args.process_performer_id)
        parameter = ProcessParameter(parameter_name=args.parameter_name, parameter_value=args.parameter_value, process_id=args.process_id)
        start_condition = ProcessStartCondition(condition_type=args.condition_type, condition_value=args.condition_value, process_id=args.process_id)
        performer = ProcessPerformer(process_performer_id=args.process_performer_id, performer_name=args.performer_name, performer_description='description')
        quota = ProcessQuota(quota_type=args.quota_type, quota_value=args.quota_value, process_id=args.process_id)
        if user_query.process_performer_id is None:
            db_session.add(performer)
        db_session.add(process)
        db_session.add(parameter)
        db_session.add(start_condition)
        db_session.add(quota)
        try:
            db_session.commit()
        except exc.IntegrityError:
            abort(404, message="Some parameters is already exist in DB")
        return args, 201


##
## Actually setup the Api resource routing here
##
api.add_resource(ProcessesList, '/processes')
api.add_resource(Processes, '/processes/<process_id>')
api.add_resource(ProcessesParameterUpdate, '/processes/update/process_parameter/<process_id>')
api.add_resource(ProcessesStartConditionUpdate, '/processes/update/process_start_condition/<process_id>')



if __name__ == '__main__':
    app.run(debug=True)





# put('http://localhost:5000/todo1', data={'data': 'Remember the milk'}).json()
#
# get('http://localhost:5000/todo1').json()


# import flask
# from flask import request, jsonify
#
# app = flask.Flask(__name__)
# app.config["DEBUG"] = True
#
# # Create some test data for our catalog in the form of a list of dictionaries.
# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]
#
#
# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Distant Reading Archive</h1>
# <p>A prototype API for distant reading of science fiction novels.</p>'''
#
#
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)
#
#
# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."
#
#     # Create an empty list for our results
#     results = []
#
#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)
#
#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)
#
# app.run()
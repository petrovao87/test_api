from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from db import db_session, Process, ProcessPerformer #ProcessParameter, ProcessQuota, ProcessStartCondition

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

# Process table
# parser.add_argument('task')
# parser.add_argument('todo_id')
parser.add_argument('process_id')# process_id todo_id
parser.add_argument('process_name')
# parser.add_argument('process_description')
# parser.add_argument('activity_flag')
parser.add_argument('process_performer_id')
#
# # ProcessParameter table
# parser.add_argument('parameter_name')
# parser.add_argument('parameter_value')
# # parser.add_argument('process_id') #####
#
# # ProcessStartCondition table
# parser.add_argument('condition_type')
# # parser.add_argument('process_id') #####
#
# # ProcessPerformer table
# # parser.add_argument('process_performer_id') ####
parser.add_argument('performer_name')
# parser.add_argument('performer_description')
#
# # ProcessQuota
# parser.add_argument('quota_type')
# parser.add_argument('quota_value')
# # parser.add_argument('process_id') #####







# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, process_id):
        # abort_if_todo_doesnt_exist(todo_id)
        # return TODOS[todo_id]
        # print(process_id)
        result = {}
        user_query = db_session.query(Process).join(ProcessPerformer).filter(Process.process_id == process_id).first()
        # print(user_query)
        result['process_id ' + str(user_query.process_id)] = {'process_name': user_query.process_name,
                                                                 'description': user_query.process_description,
                                                                 'activity_flag': user_query.activity_flag,
                                                                 'process_performer':
                                                                     {'process_performer_id': user_query.process_performer_id,
                                                                      'name': user_query.process_performer.performer_name,
                                                                      'description': user_query.process_performer.performer_description}}
        return result

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, process_id):
        args = parser.parse_args()
        user_query = db_session.query(Process).join(ProcessPerformer).filter(Process.process_id == process_id).first()
        # task = {'task': args['task']}
        a = []
        print(locals())
        for i in args:
            if args[i] is not None:
                a.append(i)
        # b = {}
        for i in a:
            print(i)
            print(user_query.process_name)
            # print(locals())
            # print(args[i])
            # user_query[i] = args[i]
            # print(user_query.i)
        # db_session.commit()
        return a, 201
        # TODOS[todo_id] = task
        # return task, 201
        # print(user_query)
        # abort_if_process_doesnt_exist(process_id, user_query)




# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        # return TODOS
        result = {}
        user_query = db_session.query(Process).join(ProcessPerformer).filter(
            Process.process_performer_id == ProcessPerformer.id).all()
        for i in range(len(user_query)):
            result['process_id ' + str(user_query[i].process_id)] = {'process_name': user_query[i].process_name,
                                                                     'description': user_query[i].process_description,
                                                                     'activity_flag': user_query[i].activity_flag,
                                                                     'process_performer':
                                                                         {'process_performer_id':
                                                                              user_query[i].process_performer_id},
                                                                     'name': user_query[i].process_performer.performer_name,
                                                                     'description': user_query[i].process_performer.performer_description}
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
        perf = ProcessPerformer(process_performer_id=args.process_id, performer_name=args.performer_name, performer_description='description')
        coin = Process(process_id=args.process_id, process_name=args.process_name, process_description='description', activity_flag='flag',
                       process_performer_id=args.process_performer_id)
        db_session.add(perf)
        db_session.add(coin)
        db_session.commit()
        return args, 201


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<process_id>')


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
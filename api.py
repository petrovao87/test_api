from flask import Flask
from sqlalchemy import exc
from flask_restful import reqparse, abort, Api, Resource
from db import db_session, Process, ProcessPerformer, ProcessParameter, ProcessQuota, ProcessStartCondition


app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Simple test-API</h1>
<h2>test_API</h2>
<p>This application allows you to work with simple API.</p>
<p> For more information visit:
https://github.com/petrovao87/test_api
</p>'''


parser = reqparse.RequestParser()

# Process table
parser.add_argument('process_id')# process_id
parser.add_argument('process_name')
parser.add_argument('process_description')
parser.add_argument('activity_flag')
parser.add_argument('process_performer_id')
#
# ProcessParameter table
parser.add_argument('parameter_name')
parser.add_argument('parameter_value')
#
# ProcessStartCondition table
parser.add_argument('condition_type')
parser.add_argument('condition_value')
#
# ProcessPerformer table
parser.add_argument('performer_name')
parser.add_argument('performer_description')
#
# ProcessQuota
parser.add_argument('quota_type')
parser.add_argument('quota_value')


# shows a single process item
class Processes(Resource):
    def get(self, process_id):
        result = {}
        user_query = db_session.query(Process).join(ProcessParameter)
        user_query = user_query.join(ProcessStartCondition)
        # print(user_query.condition_type)

        user_query = user_query.join(ProcessPerformer)
        # print(user_query.process_performer.process_performer_id)
        user_query = user_query.join(ProcessQuota).filter(Process.process_id == process_id).first()

        if user_query is not None:
            result['process_id ' + str(user_query.process_id)] = \
                {'process_id': user_query.process_id,
                 'process_name': user_query.process_name,
                 'process_description': user_query.process_description,
                 'activity_flag': user_query.activity_flag,
                 'process_parameter':
                     {'parameter_name': user_query.process_parameter[0].parameter_name,
                      'parameter_value': user_query.process_parameter[0].parameter_value},
                 'process_start_condition':
                     {'condition_type': user_query.process_start_condition[0].condition_type,
                      'condition_value': user_query.process_start_condition[0].condition_value},
                 'process_performer':
                     {'process_performer_id': user_query.process_performer_id,
                      'performer_name': user_query.process_performer.performer_name,
                      'performer_description': user_query.process_performer.performer_description},
                 'process_quota':
                     {'quota_type': user_query.process_quota[0].quota_type,
                      'quota_value': user_query.process_quota[0].quota_value}}
            return result, 200
        else:
            return abort(404, message="process {} doesn't exist".format(process_id))


# update Process table
class ProcessesUpdate(Resource):
    def put(self, process_id):
        args = parser.parse_args()
        dict_to_update = {}
        for i in args:
            if args[i] is not None:
                dict_to_update[i] = args[i]
        process_performer_id = dict_to_update.get('process_performer_id')
        user_query = db_session.query(ProcessPerformer).\
            filter(ProcessPerformer.process_performer_id == process_performer_id).first()
        if user_query is not None or process_performer_id is None:
            db_session.query(Process).filter(Process.process_id == process_id).update(dict_to_update)
            db_session.commit()
        else:
            return abort(404, message="process performer {} doesn't exist".format(process_performer_id))
        return dict_to_update, 201


# update Process Parameter table
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


# update Process Start Condition table
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


# update Process Performer table
class ProcessesPerformer(Resource):
    def put(self, process_id):
        args = parser.parse_args()
        dict_to_update = {}
        for i in args:
            if args[i] is not None:
                dict_to_update[i] = args[i]
        user_query = db_session.query(ProcessPerformer).filter(ProcessPerformer.process_performer_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(404, message="process performer {} has not this argument".format(process_id))
        result = {}
        user_query = user_query.first()
        if user_query is not None:
            db_session.commit()
            result['process_performer_id ' + str(user_query.process_performer_id)] = \
                {'process_performer_id': user_query.process_performer_id,
                 'performer_name': user_query.performer_name,
                 'performer_description': user_query.performer_description}
            return result, 201
        else:
            return abort(404, message="process {} doesn't exist".format(process_id))


# update Process Quota table
class ProcessesQuota(Resource):
    def put(self, process_id):
        args = parser.parse_args()
        dict_to_update = {}
        for i in args:
            if args[i] is not None:
                dict_to_update[i] = args[i]
        user_query = db_session.query(ProcessQuota).filter(ProcessQuota.process_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(404, message="process {} has not this argument".format(process_id))
        result = {}
        user_query = user_query.first()
        if user_query is not None:
            db_session.commit()
            result['process_id ' + str(user_query.process_id)] = \
                {'quota_type': user_query.quota_type,
                 'quota_value': user_query.quota_value}
            return result, 201
        else:
            return abort(404, message="process {} doesn't exist".format(process_id))


# shows a list of all Processes tables, and lets you POST to add new Process
class ProcessesList(Resource):
    def get(self):
        result = []
        user_query = db_session.query(Process).join(ProcessParameter)
        user_query = user_query.join(ProcessStartCondition)
        user_query = user_query.join(ProcessPerformer)
        user_query = user_query.join(ProcessQuota).all()

        for i in range(len(user_query)):
            result.append({'process_id': user_query[i].process_id,
                           'process_name': user_query[i].process_name,
                           'process_description': user_query[i].process_description,
                           'activity_flag': user_query[i].activity_flag,
                           'process_parameter':
                               {'parameter_name': user_query[i].process_parameter[0].parameter_name,
                                'parameter_value':  user_query[i].process_parameter[0].parameter_value},
                           'process_start_condition':
                               {'condition_type': user_query[i].process_start_condition[0].condition_type,
                                'condition_value': user_query[i].process_start_condition[0].condition_value},
                           'process_performer':
                               {'process_performer_id': user_query[i].process_performer.process_performer_id,
                                'performer_name': user_query[i].process_performer.performer_name,
                                'perfrmer_description': user_query[i].process_performer.performer_description},
                           'process_quota':
                               {'quota_type': user_query[i].process_quota[0].quota_type,
                                'quota_value': user_query[i].process_quota[0].quota_value}})
        return result, 200

    def post(self):
        args = parser.parse_args()
        try:
            user_query = db_session.query(ProcessPerformer).filter(ProcessPerformer.process_performer_id == args.process_performer_id).first()
            process = Process(process_id=int(args.process_id), process_name=str(args.process_name), process_description=str(args.process_description), activity_flag=str(args.activity_flag), process_performer_id=int(args.process_performer_id))
            parameter = ProcessParameter(parameter_name=str(args.parameter_name), parameter_value=str(args.parameter_value), process_id=int(args.process_id))
            start_condition = ProcessStartCondition(condition_type=str(args.condition_type), condition_value=str(args.condition_value), process_id=int(args.process_id))
            performer = ProcessPerformer(process_performer_id=int(args.process_performer_id), performer_name=str(args.performer_name), performer_description=str(args.performer_description))
            quota = ProcessQuota(quota_type=str(args.quota_type), quota_value=str(args.quota_value), process_id=int(args.process_id))
        except ValueError:
            abort(404, message="Please input correct arguments")

        if user_query is None:
            db_session.add(performer)
            # db_session.commit()
        db_session.add(start_condition)
        db_session.add(process)
        db_session.add(parameter)
        db_session.add(quota)
        try:
            db_session.commit()
        except exc.IntegrityError:
            abort(404, message="Some parameters is already exist in DB")

        return args, 200


class ProcessesDelete(Resource):
    def delete(self, process_id):
        user_query = db_session.query(Process).filter(Process.process_id == process_id)
        if len(user_query.all()) == 0:
            return abort(404, message="process {} doesn't exist".format(process_id))
        performer = user_query.first().process_performer_id
        processes_count = db_session.query(Process).filter(Process.process_performer_id == performer).all()
        if len(processes_count) > 1:
            db_session.query(Process).filter(Process.process_id == process_id).delete()
            db_session.query(ProcessParameter).filter(ProcessParameter.process_id == process_id).delete()
            db_session.query(ProcessStartCondition).filter(ProcessStartCondition.process_id == process_id).delete()
            db_session.query(ProcessQuota).filter(ProcessQuota.process_id == process_id).delete()
            db_session.commit()
        else:
            db_session.query(ProcessPerformer).filter(ProcessPerformer.process_performer_id == performer).delete()
            db_session.query(Process).filter(Process.process_id == process_id).delete()
            db_session.query(ProcessParameter).filter(ProcessParameter.process_id == process_id).delete()
            db_session.query(ProcessStartCondition).filter(ProcessStartCondition.process_id == process_id).delete()
            db_session.query(ProcessQuota).filter(ProcessQuota.process_id == process_id).delete()
            db_session.commit()
        return '', 200


#
# Actually setup the Api resource routing here
#
api.add_resource(ProcessesList, '/api/v1/processes')
api.add_resource(Processes, '/api/v1/processes/<process_id>')
api.add_resource(ProcessesUpdate, '/api/v1/processes/update/process/<process_id>')
api.add_resource(ProcessesParameterUpdate, '/api/v1/processes/update/process_parameter/<process_id>')
api.add_resource(ProcessesStartConditionUpdate, '/api/v1/processes/update/process_start_condition/<process_id>')
api.add_resource(ProcessesPerformer, '/api/v1/processes/update/process_performer/<process_id>')
api.add_resource(ProcessesQuota, '/api/v1/processes/update/process_quota/<process_id>')
api.add_resource(ProcessesDelete, '/api/v1/processes/delete/process/<process_id>')

if __name__ == '__main__':
    app.run()






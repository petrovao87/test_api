from flask_restful import abort, Resource
from db import db_session, Process, ProcessPerformer, ProcessParameter, ProcessQuota, ProcessStartCondition
from sqlalchemy import exc
from funcs import parser


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
            user_query = db_session.query(ProcessPerformer). \
                filter(ProcessPerformer.process_performer_id == args.process_performer_id).first()

            process = Process(process_id=int(args.process_id),
                              process_name=str(args.process_name),
                              process_description=str(args.process_description),
                              activity_flag=str(args.activity_flag),
                              process_performer_id=int(args.process_performer_id))
            parameter = ProcessParameter(parameter_name=str(args.parameter_name),
                                         parameter_value=str(args.parameter_value),
                                         process_id=int(args.process_id))
            start_condition = ProcessStartCondition(condition_type=str(args.condition_type),
                                                    condition_value=str(args.condition_value),
                                                    process_id=int(args.process_id))
            performer = ProcessPerformer(process_performer_id=int(args.process_performer_id),
                                         performer_name=str(args.performer_name),
                                         performer_description=str(args.performer_description))
            quota = ProcessQuota(quota_type=str(args.quota_type),
                                 quota_value=str(args.quota_value),
                                 process_id=int(args.process_id))
        except ValueError:
            abort(204, message="Please input correct arguments")

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
            abort(204, message="Some parameters is already exist in DB")

        return args, 200


# shows a single process item
class Processes(Resource):
    def get(self, process_id):
        result = {}
        user_query = db_session.query(Process).join(ProcessParameter)
        user_query = user_query.join(ProcessStartCondition)

        user_query = user_query.join(ProcessPerformer)
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
            return abort(204, message="process {} doesn't exist".format(process_id))

from flask_restful import abort, Resource
from db import db_session, Process, ProcessPerformer, ProcessParameter, ProcessQuota, ProcessStartCondition
from sqlalchemy import exc

from funcs import arg_parse


# update Process table
class ProcessesUpdate(Resource):
    def put(self, process_id):
        dict_to_update = arg_parse()
        process_performer_id = dict_to_update.get('process_performer_id')
        user_query = db_session.query(ProcessPerformer).\
            filter(ProcessPerformer.process_performer_id == process_performer_id).first()
        if user_query is not None or process_performer_id is None:
            db_session.query(Process).filter(Process.process_id == process_id).update(dict_to_update)
            db_session.commit()
        else:
            return abort(204, message="process performer {} doesn't exist".format(process_performer_id))
        return dict_to_update, 201


# update Process Parameter table
class ProcessesParameterUpdate(Resource):
    def put(self, process_id):
        dict_to_update = arg_parse()
        user_query = db_session.query(ProcessParameter).filter(ProcessParameter.process_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(204, message="process {} has not this argument".format(process_id))
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
            return abort(204, message="process {} doesn't exist".format(process_id))


# update Process Start Condition table
class ProcessesStartConditionUpdate(Resource):
    def put(self, process_id):
        dict_to_update = arg_parse()
        user_query = db_session.query(ProcessStartCondition).filter(ProcessStartCondition.process_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(204, message="process {} has not this argument".format(process_id))
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
            return abort(204, message="process {} doesn't exist".format(process_id))


# update Process Performer table
class ProcessesPerformer(Resource):
    def put(self, process_id):
        dict_to_update = arg_parse()
        user_query = db_session.query(ProcessPerformer).filter(ProcessPerformer.process_performer_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(204, message="process performer {} has not this argument".format(process_id))
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
            return abort(204, message="process {} doesn't exist".format(process_id))


# update Process Quota table
class ProcessesQuota(Resource):
    def put(self, process_id):
        dict_to_update = arg_parse()
        user_query = db_session.query(ProcessQuota).filter(ProcessQuota.process_id == process_id)
        try:
            user_query.update(dict_to_update)
        except exc.OperationalError:
            abort(204, message="process {} has not this argument".format(process_id))
        result = {}
        user_query = user_query.first()
        if user_query is not None:
            db_session.commit()
            result['process_id ' + str(user_query.process_id)] = \
                {'quota_type': user_query.quota_type,
                 'quota_value': user_query.quota_value}
            return result, 201
        else:
            return abort(204, message="process {} doesn't exist".format(process_id))
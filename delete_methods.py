from flask_restful import abort, Resource
from db import db_session, Process, ProcessPerformer, ProcessParameter, ProcessQuota, ProcessStartCondition


# DELETE process and all its parameters from tables
class ProcessesDelete(Resource):
    def delete(self, process_id):
        user_query = db_session.query(Process).filter(Process.process_id == process_id)
        if len(user_query.all()) == 0:
            return abort(204, message="process {} doesn't exist".format(process_id))
        performer = user_query.first().process_performer_id
        processes_count = db_session.query(Process).filter(Process.process_performer_id == performer).all()
        db_session.query(ProcessParameter).filter(ProcessParameter.process_id == process_id).delete()
        db_session.query(ProcessStartCondition).filter(ProcessStartCondition.process_id == process_id).delete()
        db_session.query(ProcessQuota).filter(ProcessQuota.process_id == process_id).delete()
        db_session.query(Process).filter(Process.process_id == process_id).delete()
        if len(processes_count) == 1:
            db_session.query(ProcessPerformer).filter(ProcessPerformer.process_performer_id == performer).delete()
        db_session.commit()
        return '', 200

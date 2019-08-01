from db import db_session, Process, ProcessPerformer #ProcessParameter, ProcessQuota, ProcessStartCondition


# in_db = db_session.query(Process).filter(CoinBase.coin_name == name_coin.lower()).first()
#         if not coin_in_db:
perf = ProcessPerformer(1, 'name', 'description')
coin = Process(1, 'name', 'description', 'flag', 100)
db_session.add(perf)
db_session.add(coin)
db_session.commit()
print('update base')

user_query = db_session.query(Process).join(ProcessPerformer).\
        filter(Process.process_performer_id == ProcessPerformer.id).first()
print(user_query)
# user_query.process_performer_id = 200


# activity_flag = Column(String(50))
#     process_parameter = relationship('ProcessParameter')
#     process_start_condition = relationship('ProcessParameterCondition')
#     process_performer_id = Column(Integer, ForeignKey('process_performer.id'))
#     process_performer = relationship('ProcessPerformer')
#     process_quota = relationship('ProcessQuota')
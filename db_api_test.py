from db import db_session, Process, ProcessPerformer #ProcessParameter, ProcessQuota, ProcessStartCondition
from requests import put, get, post
from flask import request, jsonify
#
#
# # in_db = db_session.query(Process).filter(CoinBase.coin_name == name_coin.lower()).first()
# #         if not coin_in_db:
#
#
#
# perf = ProcessPerformer(process_performer_id=1, performer_name='name', performer_description='description')
# coin = Process(process_id=1, process_name='name', process_description='description', activity_flag='flag',
#                process_performer_id=1)
#
# perf2 = ProcessPerformer(process_performer_id=2, performer_name='name2', performer_description='description2')
# coin2 = Process(process_id=2, process_name='name2', process_description='description2', activity_flag='flag2',
#                process_performer_id=1)
#
# coin3 = Process(process_id=3, process_name='name3', process_description='description3', activity_flag='flag3',
#                 process_performer_id=2)
#
#
# db_session.add(perf)
# db_session.add(coin)
# db_session.add(perf2)
# db_session.add(coin2)
# db_session.add(coin3)
#
# db_session.commit()
# print('update base')


result = {}
user_query = db_session.query(Process).join(ProcessPerformer).filter(Process.process_performer_id == ProcessPerformer.id).all()
print(user_query)
for i in range(len(user_query)):
    result['process_id '+str(user_query[i].process_id)] = {'process_name': user_query[i].process_name,
                                                           'process_description': user_query[i].process_description,
                                                           'activity_flag': user_query[i].activity_flag,
                                                           'process_performer':
                                                               {'process_performer_id': user_query[i].process_performer_id,
                                                                'name': user_query[i].process_performer.performer_name,
                                                                'description': user_query[i].process_performer.performer_description}}
    # print(user_query[i].process_id)
    # result['process_name '+str(user_query[i].process_name)] = user_query[i].process_name
    # print(user_query[i].process_name)

print(result)

# user_query = db_session.query(Process).join(ProcessPerformer).\
#     filter(Process.process_performer_id == 1).all()
# print(user_query)
# for i in range(len(user_query)):
#     user_query[i].process_performer_id = 2
#     print(user_query[i].process_performer_id)
#     db_session.commit()
#
# print('end')


# activity_flag = Column(String(50))
#     process_parameter = relationship('ProcessParameter')
#     process_start_condition = relationship('ProcessParameterCondition')
#     process_performer_id = Column(Integer, ForeignKey('process_performer.id'))
#     process_performer = relationship('ProcessPerformer')
#     process_quota = relationship('ProcessQuota')

# datas = ({'process_id': 111}, {'task': 'task'}, {'task2': 'task2'})
url = 'http://localhost:5000/todos'
# headers = {'Content-Type': 'application/json'}

x = post(url, data={'process_id': 111})
print(x)
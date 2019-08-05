import psycopg2

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:Passw0rd@localhost/process_db')
# engine = create_engine('sqlite:///process_db.db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Process(Base):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, unique=True)
    process_name = Column(String(50))
    process_description = Column(String())
    activity_flag = Column(String(50))
    process_parameter = relationship('ProcessParameter')
    process_start_condition = relationship('ProcessStartCondition')
    process_performer_id = Column(Integer, ForeignKey('process_performer.id'))
    # process_performer = relationship('ProcessPerformer')
    process_quota = relationship('ProcessQuota')

    def __init__(self, process_id=None, process_name=None, process_description=None, activity_flag=None, process_performer_id=None):
        self.process_id = process_id
        self.process_name = process_name
        self.process_description = process_description
        self.activity_flag = activity_flag
        self.process_performer_id = process_performer_id


class ProcessParameter(Base):
    __tablename__ = 'process_parameter'
    id = Column(Integer, primary_key=True)
    parameter_name = Column(String(50))
    parameter_value = Column(String(120))
    process_id = Column(Integer, ForeignKey('process.id'))

    def __init__(self, parameter_name=None, parameter_value=None, process_id=None):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.process_id = process_id


class ProcessStartCondition(Base):
    __tablename__ = 'process_start_condition'
    id = Column(Integer, primary_key=True)
    condition_type = Column(String(50))
    condition_value = Column(String(120))
    process_id = Column(Integer, ForeignKey('process.id'))

    def __init__(self, condition_type=None, condition_value=None, process_id=None):
        self.condition_type = condition_type
        self.condition_value = condition_value
        self.process_id = process_id


class ProcessPerformer(Base):
    __tablename__ = 'process_performer'
    id = Column(Integer, primary_key=True)
    process_performer_id = Column(Integer, unique=True)
    performer_name = Column(String(120))
    performer_description = Column(String(120))
    process_performer = relationship('Process')

    def __init__(self, process_performer_id=None, performer_name=None, performer_description=None):
        self.process_performer_id = process_performer_id
        self.performer_name = performer_name
        self.performer_description = performer_description


class ProcessQuota(Base):
    __tablename__ = 'process_quota'
    id = Column(Integer, primary_key=True)
    quota_type = Column(String(50))
    quota_value = Column(String(120))
    process_id = Column(Integer, ForeignKey('process.id'))

    def __init__(self, quota_type=None, quota_value=None, process_id=None):
        self.quota_type = quota_type
        self.quota_value = quota_value
        self.process_id = process_id


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


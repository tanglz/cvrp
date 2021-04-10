from sqlalchemy import Column, Integer, String
from db_connector import Base, db_session


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    dataset = Column(String(255))
    max_nfc = Column(Integer)
    ants = Column(Integer)
    status = Column(Integer)
    strategy = Column(String(255))
    name = Column(String(255))
    result = Column(String(255))
    task_id = Column(String(255))

    def __init__(self, dataset=None, max_nfc=None, ants=None, status=None, strategy=None, result=None, task_id=None, name=None):
        self.dataset = dataset
        self.max_nfc = max_nfc
        self.ants = ants
        self.status = status
        self.strategy = strategy
        self.results = result
        self.task_id = task_id
        self.name = name

    def query_all(self):
        result = self.query.all()
        db_session.remove()
        return result

    def query_by_id(self, id):
        result = self.query.filter_by(id=id).first()
        db_session.remove()
        return result

    def query_by_task_id(self, task_id):
        result = self.query.filter_by(task_id=task_id).first()
        db_session.remove()
        return result

    def query_by_status(self, status):
        result = self.query.filter_by(status=status).all()
        db_session.remove()
        return result

    def query_by_name(self, name):
        result = self.query.filter_by(name=name).all()
        db_session.remove()
        return result

    def update_result_by_id(self, result, id):
        task = self.query_by_id(id)
        task.result = result
        db_session.commit()
        db_session.remove()

    def update_by_task_id(self, result, status, task_id):
        task = self.query_by_task_id(task_id)
        task.result = result
        task.status = status
        db_session.commit()
        db_session.remove()

    def insert(self):
        db_session.add(self)
        db_session.commit()
        db_session.remove()
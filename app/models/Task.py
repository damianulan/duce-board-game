from app.bin.dbengine import *
from app.models.bin.BaseModel import BaseModel

class Task(BaseModel):
    id = AutoField()
    player = IntegerField()
    codename = CharField()
    finished = BooleanField(default=0)

    @staticmethod
    def migrate():
        db.create_tables([Task])

    @staticmethod
    def rollback():
        db.drop_tables([Task])

    @staticmethod
    def recreate():
        db.drop_tables([Task])
        db.create_tables([Task])
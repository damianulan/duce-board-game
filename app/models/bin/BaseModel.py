from app.bin.dbengine import *
from peewee import *

class BaseModel(Model):
    class Meta:
        database = db
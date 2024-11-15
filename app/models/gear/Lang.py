from app.bin.dbengine import *
from app.models.bin.BaseModel import BaseModel
import os
import json

class Lang(BaseModel):
    id = AutoField()
    key = CharField(unique=True)
    value = CharField()

    @staticmethod
    def factory():
        abspath = os.path.dirname(os.path.abspath(__file__))
        langpath = abspath + '/../../../datas/lang/'

        for lp in os.listdir(langpath):
            fullpath = os.path.join(langpath,lp)
            files = os.listdir(fullpath)

            for f in files:
                fp = os.path.join(fullpath, f)
                file_params = f.split('.')
                if os.path.isfile(fp):
                    with open(fp) as json_file:
                        datas = json.load(json_file)
                        if datas:
                            for key, value in datas.items():
                                if key and value:
                                    lang_key = lp+'.'+file_params[0]+'.'+ key
                                    Lang.create(key=lang_key, value=value)




    @staticmethod
    def migrate():
        db.create_tables([Lang])

    @staticmethod
    def rollback():
        db.drop_tables([Lang])

    @staticmethod
    def recreate():
        db.drop_tables([Lang])
        db.create_tables([Lang])
        Lang.factory()
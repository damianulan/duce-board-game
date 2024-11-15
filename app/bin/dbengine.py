from peewee import *
db = SqliteDatabase('datas/db/all.db')
db.connect()
#print('DB connection established')
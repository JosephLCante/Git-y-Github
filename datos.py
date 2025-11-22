
from peewee import *

db = SqliteDatabase('datos.db')

class robos(Model):
    Cedula = CharField()
    Nombre = CharField()
    fecha = CharField()
    que_se_robaron = CharField()
    valor= CharField()
    Direccion = CharField()
    lat = CharField()
    lng = CharField()
  

    class Meta:
        database = db

class Robo(Model):
    Roboid = ForeignKeyField(robos, backref='registrado')

    class Meta:
        database = db


db.connect()
db.create_tables([robos, Robo])
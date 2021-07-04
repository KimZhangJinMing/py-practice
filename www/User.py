from www.db.Field import IntField,StringField
from www.db.Model import Model


class User(Model):
    __table__ = 'users'

    id = IntField(primary_key=True)
    name = StringField()



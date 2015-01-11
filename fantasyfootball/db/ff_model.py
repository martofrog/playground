import datetime

from peewee import (
	SqliteDatabase,
	Model,
	CharField,
	IntegerField,
	FloatField,
	DateTimeField,
	ForeignKeyField,
)

from serializer import Serializer

## Find a better way of doing this
## see https://github.com/coleifer/flask-peewee/blob/master/flask_peewee/db.py
DATABASE = 'fantasyfootball.db'

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
	class Meta:
		database = database

	def as_dict(self, fields=None, exclude=None):
		return Serializer().serialize_object(self, fields, exclude)

class User(BaseModel):
	username = CharField(unique=True)
	name     = CharField(null=True)
	surname  = CharField(null=True)
	password = CharField()
	email    = CharField()
	cr_date  = DateTimeField(default=datetime.datetime.now)

	class Meta:
		order_by = ('username',)

class FFTeam(BaseModel):
	user    = ForeignKeyField(User)
	name    = CharField()
	city    = CharField()
	cr_date = DateTimeField(default=datetime.datetime.now)

	class Meta:
		order_by = ('name',)

class Season(BaseModel):
	ext_id      = IntegerField()
	name        = CharField()
	year        = IntegerField()
	league      = CharField(null=True)
	last_update = DateTimeField(default=datetime.datetime.now)

class Team(BaseModel):
	ext_id     = IntegerField()
	season     = ForeignKeyField(Season)
	name       = CharField()
	short_name = CharField(null=True)
	crest_url  = CharField(null=True)

class Player(BaseModel):
	role  = CharField()
	name  = CharField()
	birth = DateTimeField(null=True)

class PlayerTeam(BaseModel):
	player = ForeignKeyField(Player)
	team   = ForeignKeyField(Team)
	number = IntegerField(null=True)
	wage   = FloatField(null=True)
	ending = DateTimeField(null=True)

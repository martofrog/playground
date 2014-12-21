import datetime

from peewee import (
	SqliteDatabase,
	Model,
	CharField,
	DateTimeField,
	ForeignKeyField,
)

DATABASE = 'fantasyfootball.db'

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
	class Meta:
		database = database

class User(BaseModel):
	username = CharField(unique=True)
	name     = CharField()
	surname  = CharField()
	password = CharField()
	email    = CharField()
	cr_date  = DateTimeField(default=datetime.datetime.now)

	class Meta:
		order_by = ('username',)

class Team(BaseModel):
	user    = ForeignKeyField(User)
	name    = CharField()
	city    = CharField()
	cr_date = DateTimeField(default=datetime.datetime.now)

	class Meta:
		order_by = ('name',)


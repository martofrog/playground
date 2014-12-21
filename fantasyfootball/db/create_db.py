from peewee import SqliteDatabase

from ff_model import (
	User,
	Team,
)

DATABASE = 'fantasyfootball.db'

database = SqliteDatabase(DATABASE)

USERS = [
	#(username, name, password, email)
	('marione', 'Mario', 'Rossi', 'mariorossi', 'marto.socrate@tiscali.it')
]

TEAMS = [
	#(user, name, city)
	('marione', 'inter', 'Milan')
]

def create_db():
	database.connect()
	database.create_tables([
		User,
		Team,
	])

def populate():

	for user in USERS:
		u = User(
			username = user[0],
			name     = user[1],
			surname  = user[2],
			password = user[3],
			email    = user[4],
		)
		
		u.save()

		for team in TEAMS:
			if team[0] == u.username:
				t = Team(
					user = u.id,
					name = team[1],
					city = team[2],
				)

				t.save()

if __name__ == '__main__':
	create_db()
	populate()

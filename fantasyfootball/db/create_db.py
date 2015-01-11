import sys
sys.path.append("..")

from lib.api_client.football_data_org import FootballDataOrgClient

import ff_model
from ff_model import (
	User,
	FFTeam,
	Season,
	Team,
	Player,
	PlayerTeam,
)

USERS = [
	#(username, name, password, email)
	('marione', 'Mario', 'Rossi', 'mariorossi', 'marto.socrate@tiscali.it')
]

FFTEAMS = [
	#(user, name, city)
	('marione', 'inter', 'Milan')
]

PLAYERS = [
	("GK", "Gianluigi Buffon",   "28 Jan 1978", "Juventus"),
	("GK", "Salvatore Sirigu",   "12 Jan 1987", "Cagliari"),
	("GK", "Federico Marchetti", "7 Feb 1983",  "Lazio"),
	("GK", "Mattia Perin",       "10 Nov 1992", "Genoa"),
	("GK", "Marco Storari",      "7 Jan 1977",  "Juventus"),

	("DF", "Christian Maggio",   "11 Feb 1982", "Napoli"),
	("DF", "Giorgio Chiellini",  "14 Aug 1984", "Juventus"),
	("DF", "Davide Astori",      "7 Jan 1987",  "Roma"),
	("DF", "Mattia De Sciglio",  "20 Oct 1992", "Milan"),
	("DF", "Andrea Barzagli",    "8 May 1981",  "Juventus"),
	("DF", "Leonardo Bonucci",   "1 May 1987",  "Juventus"),
	("DF", "Ignazio Abate",      "12 Nov 1986", "Milan"),
	("DF", "Andrea Ranocchia",   "16 Feb 1988", "Inter"),
	("DF", "Manuel Pasqual",     "13 Mar 1982", "Fiorentina"),
	("DF", "Gabriel Paletta",    "15 Feb 1986", "Parma"),
	("DF", "Matteo Darmian",     "2 Dec 1989",  "Torino"),
	("DF", "Angelo Ogbonna",     "25 May 1988", "Juventus"),

	("MF", "Antonio Candreva",     "28 Feb 1987", "Lazio"),
	("MF", "Alberto Aquilani",     "7 Jul 1984",  "Fiorentina"),
	("MF", "Claudio Marchisio",    "19 Jan 1986", "Juventus"),
	("MF", "Daniele De Rossi",     "24 Jul 1983", "Roma"),
	("MF", "Riccardo Montolivo",   "18 Jan 1985", "Milan"),
	("MF", "Andrea Pirlo",         "19 May 1979", "Juventus"),
	("MF", "Emanuele Giaccherini", "5 May 1985",  "Juventus"),
	("MF", "Alessandro Diamanti",  "2 May 1983",  "Torino"),
	("MF", "Thiago Motta",         "28 Aug 1982", "Juventus"),
	("MF", "Marco Verratti",       "5 Nov 1992",  "Inter"),
	("MF", "Marco Parolo",         "25 Jan 1985", "Parma"),
	("MF", "Romulo",               "22 May 1987", "Verona"),
	("MF", "Simone Pepe",          "30 Aug 1983", "Juventus"),
	("MF", "Claudio Marchisio",    "19 Jan 1986", "Juventus"),
	("MF", "Simone Padoin",        "18 Mar 1984", "Juventus"),
	("MF", "Luca Marrone",         "28 Mar 1990", "Juventus"),

	("FW", "Mario Balotelli",     "12 Aug 1990",  "Milan"),
	("FW", "Sebastian Giovinco",  "26 Jan 1987",  "Juventus"),
	("FW", "Alberto Gilardino",   "5 Jul 1982",   "Milan"),
	("FW", "Stephan El Shaarawy", "27 Oct 1992",  "Milan"),
	("FW", "Alessio Cerci",       "23 Jul 1987",  "Torino"),
	("FW", "Antonio Cassano",     "12 July 1982", "Parma"),
	("FW", "Giuseppe Rossi",      "1 Feb 1987",   "Fiorentina"),
	("FW", "Mattia Destro",       "20 Mar 1991",  "Roma"),
	("FW", "Lorenzo Insigne",     "4 Jun 1991",   "Napoli"),
	("FW", "Ciro Immobile",       "20 Feb 1990",  "Torino"),
	("FW", "Fabio Borini",        "29 Mar 1991",  "Roma"),

]

def create_db():
	database = ff_model.database

	database.connect()
	database.create_tables([
		User,
		FFTeam,
		Season,
		Team,
		Player,
		PlayerTeam,
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

		for team in FFTEAMS:
			if team[0] == u.username:
				t = FFTeam(
					user = u.id,
					name = team[1],
					city = team[2],
				)

				t.save()

	fdo = FootballDataOrgClient()

	api_season = fdo.get_season("Serie A")

	season = Season(
		ext_id = api_season.get('id'),
		name   = api_season.get('caption'),
		year   = api_season.get('year'),
		league = api_season.get('league'),
	)

	season.save()

	api_teams = fdo.get_season_teams(season.ext_id).json()

	for t in api_teams:
		team = Team(
			ext_id     = t.get('id'),
			season     = season.id,
			name       = t.get('name'),
			short_name = t.get('shortName'),
			crest_url  = t.get('crestUrl'),
		)

		team.save()

	##Here load season and teams from API

if __name__ == '__main__':

	create_db()
	populate()

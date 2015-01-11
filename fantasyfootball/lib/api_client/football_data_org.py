import logging
import requests

def do_get(base_url, path, params, headers):
	url = base_url + path
	res = requests.get(url, params=params, headers=headers)

	return res

class FootballDataOrgClient():
	def __init__(self, cfg=None):
		if not cfg:
			cfg = {}

		self.base_url = cfg.get("base_url", "http://www.football-data.org/")
		self.headers  = cfg.get("headers", dict())

	def get_seasons(self):
		path   = "soccerseasons"
		params = dict()

		res  = do_get(
			base_url = self.base_url,
			path     = path,
			params   = params,
			headers  = self.headers,
		)

		return res

	def get_season(self, league_name):
		res = self.get_seasons()

		season = filter(lambda x : league_name in x['caption'], res.json())[0]

		logging.debug("season = %s", season)

		return season

	def get_season_ranking(self, season_id, matchday=None):
		path   = "soccerseasons/" + str(season_id) + "/ranking"
		params = dict(
			matchday = matchday,
		)

		res  = do_get(
			base_url = self.base_url,
			path     = path,
			params   = params,
			headers  = self.headers,
		)

		return res

	def get_season_teams(self, season_id):
		path   = "soccerseasons/" + str(season_id) + "/teams"
		params = dict()

		res  = do_get(
			base_url = self.base_url,
			path     = path,
			params   = params,
			headers  = self.headers,
		)

		return res

	def get_team(self, season_id, team_id=None, team_name=None):
		if team_id is None:
			res = self.get_season_teams(season_id)

			team = filter(lambda x : team_name in x['name'], res.json())[0]

		else:

			path   = "teams/" + str(team_id)
			params = dict()

			res  = do_get(
				base_url = self.base_url,
				path     = path,
				params   = params,
				headers  = self.headers,
			)

			team = res.json()

		logging.debug("team = %s", team)

		return team

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	cfg = dict(
		base_url = "http://www.football-data.org/",
		headers  = {
			"Auth-Token" : "3405775701cc443085d945e96b5ff8ae",
		},
	)

	fdo_client = FootballDataOrgClient(cfg)

	season = fdo_client.get_season("Serie A")

	#res = fdo_client.get_season_ranking(season['id'])

	team = fdo_client.get_team(season['id'], team_name='Juve')

	logging.debug("team %s", team)

	#team = fdo_client.get_team(season['id'], team_id=109)

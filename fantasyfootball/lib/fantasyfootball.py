import tornado
import tornado.web
import tornado.auth

import json
from bson import json_util

from db import ff_model

from db.ff_model import (
	User,
	Season,
	Team
)

class FantasyFootballApp(tornado.web.Application):
	def __init__(self, options):
		handlers = [
			(r"/",              HomeHandler),
			(r"/index",         IndexHandler),
			(r"/api/v1/season", SeasonHandler),
			(r"/api/v1/team",   TeamHandler),
			(r"/api/v2/player", PlayerHandler),
			(r"/auth/login",    AuthLoginHandler),
			(r"/auth/logout",   AuthLogoutHandler),
		]

		settings = dict(
			title         = "Fantasy Football",
			template_path = options.template_path,
			static_path   = options.static_path,
			xsrf_cookies  = True,
			cookie_secret = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
			login_url     = "/auth/login",
			debug         = True,
			#ui_modules={"Entry": EntryModule},
		)

		self.db = ff_model.database
		self.db.connect()

		tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		user_id = self.get_secure_cookie("user")
		if not user_id: return None
		
		return User(id=user_id)

class HomeHandler(BaseHandler):
	def get(self):
		self.render("home.html")

class IndexHandler(BaseHandler):
	def get(self):
		self.render("index.html")

class SeasonHandler(BaseHandler):
	def get(self):
		seasons = Season.select()

		season = seasons[0]	
		teams  = Team.select().where(Team.season==season.id)

		ctx = dict(
			season = season.as_dict(),
			teams  = [t.as_dict() for t in teams],
		)

		self.set_header("Content-Type", "application/json")
		self.write(json.dumps(ctx, default=json_util.default))

class TeamHandler(BaseHandler):
	def get(self):
		pass

class PlayerHandler(BaseHandler):
	def get(self):
		pass

class LoginHandler(BaseHandler):
	pass

class LogoutHandler(BaseHandler):
	pass

class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
	@tornado.web.asynchronous
	def get(self):
		if self.get_argument("openid.mode", None):
			self.get_authenticated_user(self._on_auth)
			return
		self.authenticate_redirect()

	def _on_auth(self, user):
		if not user:
			raise tornado.web.HTTPError(500, "Google auth failed")
		
		usr = User(email=user["email"])

		if not usr:
			# Auto-create first author
			any_author = self.db.get("SELECT * FROM authors LIMIT 1")
			if not any_author:
				user_id = self.db.execute(
					"INSERT INTO authors (email,name) VALUES (%s,%s)",
					user["email"], user["name"])
			else:
				self.redirect("/")
				return
		else:
			user_id = usr["id"]

		self.set_secure_cookie("user", str(user_id))
		self.redirect(self.get_argument("next", "/"))

class AuthLogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect(self.get_argument("next", "/"))

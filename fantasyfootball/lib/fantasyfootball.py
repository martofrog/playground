import tornado
import tornado.web
import tornado.auth

from peewee import SqliteDatabase

from db.ff_model import (
	User,
)

class FantasyFootballApp(tornado.web.Application):
	def __init__(self, options):
		handlers = [
			(r"/",            HomeHandler),
			(r"/auth/login",  AuthLoginHandler),
			(r"/auth/logout", AuthLogoutHandler),
		]

		settings = dict(
			title="Fantasy Football",
			template_path=options.template_path,
			static_path=options.static_path,
			#ui_modules={"Entry": EntryModule},
			xsrf_cookies=True,
			cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
			login_url="/auth/login",
			debug=True,
		)

		tornado.web.Application.__init__(self, handlers, **settings)

		self.db = SqliteDatabase(options.database)
		self.db.connect()

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		self.application.db

	def get_current_user(self):
		user_id = self.get_secure_cookie("user")
		if not user_id: return None
		
		return User(id=user_id)

class HomeHandler(BaseHandler):
	def get(self):
		self.render("home.html")

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

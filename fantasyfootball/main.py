import os
import tornado
import tornado.httpserver

from tornado.options import (
	options,
	define,
)

from lib.fantasyfootball import FantasyFootballApp

define("port", default=8888, help="run on the given port", type=int)
define("database", default="fantasyfootbal.db", help="blog database name")
define("template_path", default=os.path.join(os.path.dirname(__file__), "template"))
define("static_path", default=os.path.join(os.path.dirname(__file__), "static"))

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(FantasyFootballApp(options))
	http_server.listen(options.port)

	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()

import tornado
import tornado.httpserver

from tornado.options import (
	options,
	define,
)

from lib.fantasyfootball import FantasyFootballApp

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(FantasyFootballApp())
	http_server.listen(options.port)

	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()

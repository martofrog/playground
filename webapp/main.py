# all the imports
import sqlite3
from flask import (
	Flask,
	request,
	session,
	g,
	redirect,
	url_for,
	abort,
	render_template,
	flash,
)

# configuration
DATABASE   = 'db/flaskr.db'
DEBUG      = True
SECRET_KEY = 'development key'
USERNAME   = 'admin'
PASSWORD   = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]

    return render_template('show_entries.html', entries=entries)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
	app.run(host='0.0.0.0')



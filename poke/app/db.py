import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
        host=current_app.config['DATABASE_HOST'],     # ✅ sin FLASK_
        user=current_app.config['DATABASE_USER'],
        password=current_app.config['DATABASE_PASSWORD'],
        database=current_app.config['DATABASE'],
        port=int(current_app.config['DATABASE_PORT'])
        )

        g.c = g.db.cursor(dictionary=True)

    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

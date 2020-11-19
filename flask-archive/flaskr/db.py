import psycopg2, psycopg2.extras
from os import environ
import click
from flask import current_app,g
from flask.cli import with_appcontext

#postgrSQL database class
class Database:
    def __init__(self):
        self.host=environ.get('DATABASE_HOST')
        self.username=environ.get('DATABASE_USERNAME')
        self.password=environ.get('DATABASE_PASSWORD')
        self.dbname=environ.get('DATABASE_NAME')

def get_db():
    config=Database()
    if 'db' not in g:
        g.db=psycopg2.connect(
            host=config.host,
            user=config.username,
            password=config.password,
            dbname=config.dbname,
            cursor_factory=psycopg2.extras.DictCursor
        )
        g.db.autocommit=True
    return g.db.cursor()

def close_db(e=None):
    db=g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db=get_db()

    with current_app.open_resources('schema.sql','rt') as f:
        text=f.read()
        db.execute(text)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

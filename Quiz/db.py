import mysql.connector
from mysql.connector import Error
from flask import current_app, g
import click
import email_validator



def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="01101997Programmer10?",
        database="mydb"
    )

    if not db.is_connected():
        raise ConnectionError("could not connect to db")

    db_info = db.get_server_info()
    print("server: ", db_info)
    cursor = db.cursor()
    cursor.execute("SELECT DATABASE();")
    database_name = cursor.fetchone()
    print("Connected to: ", database_name)
    return db


def close_db(db):
    connect_db().close


def init_db():
    db = connect_db()
    with open("Quiz\schema.sql", 'r') as f:
        sqlf = f.read()
        f.close()
    sql_commands = sqlf.split(";")
    for command in sql_commands:
        cursor = db.cursor()
        cursor.execute(command)
    db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Initizing the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
import os
import tempfile

import pytest
from Quiz import create_app
from Quiz.db import connect_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')
    print(_data_sql)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
    })
    with app.app_context():
        init_db()
        db = connect_db()
        sql_commands = _data_sql.split(";")
        for command in sql_commands:
            cursor = db.cursor()
            cursor.execute(command)
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

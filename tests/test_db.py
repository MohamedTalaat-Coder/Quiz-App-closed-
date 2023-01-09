import pytest
import mysql.connector
from mysql.connector import Error
from Quiz.db import connect_db

def test_connect_close_db(app):
    with app.app_context():
        db = connect_db()
        assert db.is_connected() == True
    with pytest.raises(mysql.connector.ProgrammingError) as err:
        cursor = db.cursor()
        cursor.execute("select name")
    assert "Unknown column 'name'" in str(err.value)


def test_init_db_command(runner, monkeypatch):
    class Record(object):
        called = False
    def fake_init_db():
        Record.called = True
    
    monkeypatch.setattr('Quiz.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initizing' in result.output
    assert Record.called

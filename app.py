from flask import Flask
from todolist import todolist_view
import sqlite3

app = Flask(__name__)


def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_tables():
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL, 
                content TEXT NOT NULL
        );"""]
    # create a database connection
    try:
        with sqlite3.connect('my.db') as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    create_sqlite_database("my.db")
    create_tables()
    app.register_blueprint(todolist_view)
    app.run(debug=True)

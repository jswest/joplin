import sqlite3
from contextlib import contextmanager
from typing import Generator

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    try:
        connection = sqlite3.connect('./db/joplin.db')
        connection.enable_load_extension(True)
        connection.load_extension("vector0")
        
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        
        yield connection
        connection.commit()
 
    except Exception as e:
        print(e)
        raise e
    finally:
        connection.close()

def init_db() -> None:    
    try:
        with get_db() as connection:
            with open('./db/schema.sql', 'r') as in_file:
                sql = in_file.read()
            connection.executescript(sql)
    except Exception as e:
        print(e)
        raise e

if __name__ == "__main__":
    init_db()
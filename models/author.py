from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if id is None:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
                conn.commit()
                self.id = cursor.lastrowid
                self._name = name
        else:
            self.id = id
            self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 1:
            raise ValueError("Name must be a non-empty string.")
        self._name = value


from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
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

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
            conn.commit()
            self.id = cursor.lastrowid

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT articles.id, articles.title
                FROM articles
                WHERE articles.author_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def magazines(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT magazines.id, magazines.name
                FROM magazines
                JOIN articles ON articles.magazine_id = magazines.id
                WHERE articles.author_id = ?
            """, (self.id,))
            return cursor.fetchall()

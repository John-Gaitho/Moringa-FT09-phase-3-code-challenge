
from database.connection import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self.id = id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        self._title = value

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO articles (title, content, author_id, magazine_id) 
                VALUES (?, ?, ?, ?)
            """, (self._title, self.content, self.author_id, self.magazine_id))
            conn.commit()
            self.id = cursor.lastrowid

    @property
    def author(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.name
                FROM authors
                JOIN articles ON articles.author_id = authors.id
                WHERE articles.id = ?
            """, (self.id,))
            author = cursor.fetchone()
            return author if author else None

    @property
    def magazine(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT magazines.name
                FROM magazines
                JOIN articles ON articles.magazine_id = magazines.id
                WHERE articles.id = ?
            """, (self.id,))
            magazine = cursor.fetchone()
            return magazine if magazine else None

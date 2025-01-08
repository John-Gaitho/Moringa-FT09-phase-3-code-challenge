from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self._name = name
        self._category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) <= 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def create(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
            conn.commit()
            self.id = cursor.lastrowid

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT articles.id, articles.title
                FROM articles
                WHERE articles.magazine_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def contributors(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.id, authors.name
                FROM authors
                JOIN articles ON articles.author_id = authors.id
                WHERE articles.magazine_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def article_titles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT articles.title
                FROM articles
                WHERE articles.magazine_id = ?
            """, (self.id,))
            titles = cursor.fetchall()
            return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.id, authors.name
                FROM authors
                JOIN articles ON articles.author_id = authors.id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING COUNT(articles.id) > 2
            """, (self.id,))
            return cursor.fetchall()

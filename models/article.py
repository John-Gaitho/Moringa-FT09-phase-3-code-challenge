import sqlite3

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"<Article {self.title}>"

    @property
    def author(self):
        conn = sqlite3.connect('magazine.db')
        c = conn.cursor()
        c.execute("""
        SELECT authors.name
        FROM authors
        JOIN articles ON articles.author_id = authors.id
        WHERE articles.id = ?
        """, (self.id,))
        author = c.fetchone()
        conn.close()
        return author if author else None

    @property
    def magazine(self):
        conn = sqlite3.connect('magazine.db')
        c = conn.cursor()
        c.execute("""
        SELECT magazines.name
        FROM magazines
        JOIN articles ON articles.magazine_id = magazines.id
        WHERE articles.id = ?
        """, (self.id,))
        magazine = c.fetchone()
        conn.close()
        return magazine if magazine else None

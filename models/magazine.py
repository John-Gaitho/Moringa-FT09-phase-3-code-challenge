from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id is None:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
                conn.commit()
                self.id = cursor.lastrowid
                self._name = name
                self._category = category
        else:
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
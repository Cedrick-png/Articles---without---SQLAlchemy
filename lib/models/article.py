from lib.db.connection import get_connection

class Article:
    def __init__(self, title: str, author=None, magazine=None, id=None):
        self._id = id
        self._title = title
        self._author_id = author.id if hasattr(author, 'id') else author
        self._magazine_id = magazine.id if hasattr(magazine, 'id') else magazine

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self._title, self._author_id, self._magazine_id, self._id)
                )
            else:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self._title, self._author_id, self._magazine_id)
                )
                self._id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row["title"], row["author_id"], row["magazine_id"], row["id"])
            return None
        finally:
            conn.close()

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
            if row:
                return cls(row["title"], row["author_id"], row["magazine_id"], row["id"])
            return None
        finally:
            conn.close()

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
            rows = cursor.fetchall()
            return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]
        finally:
            conn.close()

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
            rows = cursor.fetchall()
            return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]
        finally:
            conn.close()
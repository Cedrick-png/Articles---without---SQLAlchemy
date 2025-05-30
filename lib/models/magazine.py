from lib.db.connection import get_connection
from typing import List, Optional

class Magazine:
    def __init__(self, name: str, category: str, id: Optional[int] = None):
        if not name or not isinstance(name, str):
            raise ValueError("Magazine name must be a non-empty string")
        if not category or not isinstance(category, str):
            raise ValueError("Category must be a non-empty string")
        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self._name, self._category)
                )
                self._id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self._name, self._category, self._id)
                )
            conn.commit()
        finally:
            conn.close()

    def articles(self) -> List['Article']:
        from lib.models.article import Article
        return Article.find_by_magazine(self._id)

    def article_titles(self) -> List[str]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
            return [row["title"] for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["category"], row["id"])
            return None
        finally:
            conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["category"], row["id"])
            return None
        finally:
            conn.close()

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
            rows = cursor.fetchall()
            return [cls(row["name"], row["category"], row["id"]) for row in rows]
        finally:
            conn.close()
from lib.db.connection import get_connection
from typing import List, Optional
from lib.models.magazine import Magazine

class Author:
    def __init__(self, name: str, id: Optional[int] = None):
        if not name or not isinstance(name, str):
            raise ValueError("Author name must be a non-empty string")
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
                self._id = cursor.lastrowid
            else:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self._id))
            conn.commit()
        finally:
            conn.close()

    def articles(self) -> List['Article']:
        from lib.models.article import Article
        return Article.find_by_author(self._id)

    def magazines(self) -> List['Magazine']:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT magazines.* FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
            """, (self._id,))
            rows = cursor.fetchall()
            return [Magazine(row["name"], row["category"], row["id"]) for row in rows]
        finally:
            conn.close()

    def add_article(self, magazine: 'Magazine', title: str) -> 'Article':
        from lib.models.article import Article
        article = Article(title=title, author=self, magazine=magazine)
        article.save()
        return article

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["id"])
            return None
        finally:
            conn.close()
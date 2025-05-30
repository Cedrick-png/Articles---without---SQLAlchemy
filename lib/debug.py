from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def magazines_with_multiple_authors() -> List[Dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id, m.name, m.category
            HAVING COUNT(DISTINCT a.author_id) >= 2
            """
        )
        return [
            {"id": row['id'], "name": row['name'], "category": row['category']}
            for row in cursor.fetchall()
        ]

def article_counts_by_magazine() -> List[Dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id, m.name, m.category
            """
        )
        return [
            {"id": row['id'], "name": row['name'], "category": row['category'], "article_count": row['article_count']}
            for row in cursor.fetchall()
        ]

def most_prolific_author() -> Optional[Dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT a.id, a.name, COUNT(art.id) as article_count
            FROM authors a
            LEFT JOIN articles art ON a.id = art.author_id
            GROUP BY a.id, a.name
            ORDER BY article_count DESC
            LIMIT 1
            """
        )
        result = cursor.fetchone()
        return {"id": result['id'], "name": result['name'], "article_count": result['article_count']} if result else None

def add_author_with_articles(author_name: str, articles_data: List[Dict]) -> bool:
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (author_name,)
        )
        author_id = cursor.lastrowid
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        conn.execute("COMMIT")
        return True
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()
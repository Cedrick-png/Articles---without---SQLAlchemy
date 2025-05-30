import pytest
import sqlite3
import logging
from lib.db.connection import get_connection
from scripts.setup_db import setup_database
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    logging.debug("Running setup_db fixture")
    setup_database()
    yield

@pytest.fixture(autouse=True)
def setup_and_teardown(setup_db):
    logging.debug("Running setup_and_teardown fixture")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM articles")
        conn.commit()
    except sqlite3.OperationalError as e:
        logging.error(f"Failed to clear articles: {e}")
        raise
    finally:
        conn.close()
    yield

def test_save_and_find_by_id():
    author = Author("John Doe")
    author.save()
    magazine = Magazine("Tech Today", "Technology")
    magazine.save()
    article = Article("Test Article", author, magazine)
    article.save()
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"
    assert found.author_id == author.id
    assert found.magazine_id == magazine.id

def test_find_by_title():
    author = Author("Jane Smith")
    author.save()
    magazine = Magazine("Science Weekly", "Science")
    magazine.save()
    article = Article("Unique Article", author, magazine)
    article.save()
    found = Article.find_by_title("Unique Article")
    assert found is not None
    assert found.title == "Unique Article"

def test_find_by_author():
    author = Author("Bob Johnson")
    author.save()
    magazine = Magazine("Tech Today", "Technology")
    magazine.save()
    article = Article("Author Test", author, magazine)
    article.save()
    found = Article.find_by_author(author.id)
    assert len(found) > 0
    assert found[0].title == "Author Test"

def test_find_by_magazine():
    author = Author("John Doe")
    author.save()
    magazine = Magazine("Science Weekly", "Science")
    magazine.save()
    article = Article("Magazine Test", author, magazine)
    article.save()
    found = Article.find_by_magazine(magazine.id)
    assert len(found) > 0
    assert found[0].title == "Magazine Test"
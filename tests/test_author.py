import pytest
import logging
import sqlite3
from lib.db.connection import get_connection
from scripts.setup_db import setup_database
from lib.models.author import Author
from lib.models.magazine import Magazine

logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    logging.debug("Running setup_db fixture")
    setup_database()
    yield

@pytest.fixture(autouse=True)
def setup_and_teardown_db(setup_db):
    logging.debug("Running setup_and_teardown_db fixture")
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

def test_create_and_find_author():
    author = Author("Test Author")
    author.save()
    found = Author.find_by_name("Test Author")
    assert found is not None
    assert found.name == "Test Author"

def test_articles_and_magazines_relationship():
    author = Author("Test Author")
    author.save()
    magazine = Magazine("Test Mag", "Tech")
    magazine.save()
    article = author.add_article(magazine, "Test Article")
    articles = author.articles()
    magazines = author.magazines()
    assert len(articles) > 0
    assert len(magazines) > 0
    assert articles[0].title == "Test Article"  # Corrected line

def test_add_article_method():
    author = Author("Test Author")
    author.save()
    magazine = Magazine("Test Mag", "Tech")
    magazine.save()
    article = author.add_article(magazine, "New Article")
    assert article.title == "New Article"
    assert article.author_id == author.id
    assert article.magazine_id == magazine.id
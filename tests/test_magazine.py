import pytest
import logging
from lib.db.connection import get_connection
from scripts.setup_db import setup_database
from lib.models.magazine import Magazine
from lib.models.author import Author

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
        cursor.execute("DELETE FROM magazines")
        conn.commit()
    except sqlite3.OperationalError as e:
        logging.error(f"Failed to clear magazines: {e}")
        raise
    finally:
        conn.close()
    yield

def test_save_and_find_by_id():
    magazine = Magazine("Test Mag", "Tech")
    magazine.save()
    found = Magazine.find_by_id(magazine.id)
    assert found is not None
    assert found.name == "Test Mag"

def test_find_by_name():
    magazine = Magazine("Unique Mag", "Science")
    magazine.save()
    found = Magazine.find_by_name("Unique Mag")
    assert found is not None
    assert found.name == "Unique Mag"

def test_find_by_category():
    magazine = Magazine("Category Mag", "Tech")
    magazine.save()
    found = Magazine.find_by_category("Tech")
    assert len(found) > 0
    assert found[0].name == "Category Mag"

def test_article_titles_empty():
    magazine = Magazine("Empty Mag", "Tech")
    magazine.save()
    titles = magazine.article_titles()
    assert titles == []
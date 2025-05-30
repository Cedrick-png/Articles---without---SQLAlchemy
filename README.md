# Articles---without---SQLAlchemy
Setup Instructions





Ensure Python 3.8+ and SQLite3 are installed



Install pytest: pip install pytest



Clone the repository



Navigate to the project directory:

cd /path/to/Articles---without---SQLAlchemy



Run the setup script to create and seed the database:

python scripts/setup_db.py



Run tests with:

pytest tests



Run example queries with:

python scripts/run_queries.py



Use python lib/debug.py for interactive debugging

Features





Complete ORM implementation for Author, Magazine, and Article



SQLite3 database with proper relationships and indexes



Transaction handling with context managers



Protection against SQL injection



Comprehensive test suite using pytest



Seed data for testing



CLI interface for interactive querying



Efficient SQL queries for all relationships

Running Tests

pytest tests

For verbose output:

pytest tests -v

Example Usage

from lib.models.author import Author
from lib.models.magazine import Magazine

# Create and save an author
author = Author("John Doe")
author.save()

# Create and save a magazine
magazine = Magazine("Tech Today", "Technology")
magazine.save()

# Add an article
article = author.add_article(magazine, "Tech Trends 2025")

Notes





Ensure python scripts/setup_db.py is run before tests to create the database and tables.



All database operations use parameterized queries for security.



Foreign keys with ON DELETE CASCADE ensure data integrity.



Indexes improve query performance.



Test suite covers all major functionality.



Seed data provides realistic test cases.
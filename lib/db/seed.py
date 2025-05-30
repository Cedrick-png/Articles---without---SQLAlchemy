from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
import logging

logging.basicConfig(level=logging.DEBUG)

def seed_database():
    logging.debug("Starting seed_database")
    author1 = Author("John Doe")
    author2 = Author("Jane Smith")
    author3 = Author("Bob Johnson")
    author1.save()
    author2.save()
    author3.save()

    mag1 = Magazine("Tech Today", "Technology")
    mag2 = Magazine("Science Weekly", "Science")
    mag1.save()
    mag2.save()

    author1.add_article(mag1, "Tech Trends 2025")
    author1.add_article(mag2, "AI Revolution")
    author2.add_article(mag1, "Quantum Computing")
    author2.add_article(mag2, "Climate Change Solutions")
    author3.add_article(mag1, "Blockchain Basics")

    logging.debug("Seed data completed")

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully")
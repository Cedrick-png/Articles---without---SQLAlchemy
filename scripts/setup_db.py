import sqlite3

def setup_database():
    with open('lib/db/schema.sql') as f:
        schema = f.read()
    
    conn = sqlite3.connect('articles.db')
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
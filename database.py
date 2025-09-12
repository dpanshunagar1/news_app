import os
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv  

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create a new database connection"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    return psycopg2.connect(DATABASE_URL)

def truncate_articles():
    """Clean the entire articles table and reset IDs"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("TRUNCATE TABLE articles RESTART IDENTITY CASCADE;")
        conn.commit()
        print("🧨 Articles table truncated (IDs reset).")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error truncating table: {e}")
    finally:
        cur.close()
        conn.close()

def fetch_all_articles():
    """Fetch all articles from the articles table"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM articles;")
        articles = cur.fetchall()
        return articles
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_rss_feeds():
    """Fetch all RSS feed URLs from Supabase 'rss' table"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT url FROM rss;")
        feeds = cur.fetchall()
        return feeds
    except Exception as e:
        print(f"❌ Error fetching RSS feeds from database: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def insert_articles(articles):
    """Insert multiple articles into the articles table"""
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
    INSERT INTO articles (title, link, summary, content, author, published, updated, categories, thumbnail_url, relevence)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (link) DO NOTHING;
    """
    try:
        execute_batch(cur, sql, articles)
        conn.commit()
        print(f"✅ Inserted {cur.rowcount} new articles.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting articles: {e}")
    finally:
        cur.close()
        conn.close()

def create_new_table():
    """Create rss_articles table"""
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """ CREATE TABLE IF NOT EXISTS rss_articles(
            id BIGSERIAL PRIMARY KEY,
            title TEXT,
            link TEXT UNIQUE,
            published TIMESTAMPTZ
        );"""
    try:
        cur.execute(sql)
        conn.commit()
        print("✅ Table rss_articles created successfully.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creating table: {e}")
    finally:
        cur.close()
        conn.close()

def insert_rss_articles(articles):
    """Insert multiple articles into the rss_articles table"""
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
    INSERT INTO rss_articles (title, link, published)
    VALUES (%s, %s, %s)
    ON CONFLICT (link) DO NOTHING;
    """
    try:
        execute_batch(cur, sql, articles)
        conn.commit()
        print(f"✅ Inserted {len(articles)} new articles.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting articles: {e}")
    finally:
        cur.close()
        conn.close()

def get_urls_for_article():
    """Get all article URLs from rss_articles table"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT link FROM rss_articles;")
        feeds = cur.fetchall()
        return feeds
    except Exception as e:
        print(f"❌ Error fetching article URLs from database: {e}")
        return []
    finally:
        cur.close()
        conn.close()
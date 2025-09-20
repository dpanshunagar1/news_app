#!/usr/bin/env python3
"""
Enhanced RSS + newspaper3k Article Fetcher

Combines RSS feed discovery with newspaper3k's powerful content extraction.
This gives you the best of both worlds: RSS metadata + clean article content.
"""

import os
import feedparser
from newspaper import Article
from dotenv import load_dotenv
from datetime import datetime
from app import create_app, get_db_session
from app.models import Article as ArticleModel
from database import truncate_articles ,get_rss_feeds # Reuse existing truncate function

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def extract_with_newspaper3k(url):
    """Extract clean article content using newspaper3k"""
    try:
        # Create newspaper3k article object
        article = Article(url)
        article.download()
        article.parse()
        
        # Apply NLP for keywords and summary
        try:
            article.nlp()
        except:
            pass  # NLP might fail, but other data is still usable
        
        return {
            'title': article.title or 'No Title',
            'text': article.text or '',  # Clean text, no HTML!
            'summary': article.summary or '',
            'authors': article.authors or [],
            'publish_date': article.publish_date,
            'top_image': article.top_image or '',
            'keywords': article.keywords or [],
            'meta_keywords': article.meta_keywords or [],
            'canonical_link': article.canonical_link or url
        }
    except Exception as e:
        print(f"  ⚠️ newspaper3k extraction failed for {url}: {e}")
        return None

def fetch_articles_from_feed(feed_url):
    print(f"📡 Fetching from: {feed_url}")
    
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            print(f"⚠️ Warning: Feed may have parsing issues - {feed.bozo_exception}")
        
        articles = []
        for entry in feed.entries:  # Limit to 10 articles per feed for demo
            
            # Get basic RSS data
            rss_title = getattr(entry, 'title', 'No Title')
            link = getattr(entry, 'link', '')
            
            if not link:
                print(f"  ⏭️ Skipping article with no link: {rss_title[:50]}...")
                continue
            
            print(f"  📄 Processing: {rss_title[:60]}...")
            
            # Extract enhanced data with newspaper3k
            newspaper_data = extract_with_newspaper3k(link)
            
            if not newspaper_data:
                # Fallback to RSS data if newspaper3k fails
                articles.append({
                    "title": rss_title,
                    "link": link,
                    "summary": getattr(entry, 'summary', ''),
                    "content": '',
                    "author": getattr(entry, 'author', None),
                    "published_parsed": getattr(entry, 'published_parsed', None),
                    "updated_parsed": getattr(entry, 'updated_parsed', None),
                    "categories": ','.join([tag.term for tag in getattr(entry, 'tags', [])]),
                    "source_feed": feed_url,
                    "guid": getattr(entry, 'id', link),
                    "language": getattr(entry, 'language', None),
                    "thumbnail_url": None,
                    "keywords": None
                })
                continue
            
            # Combine RSS metadata with newspaper3k content
            articles.append({
                "title": newspaper_data['title'] or rss_title,
                "link": link,
                "summary": newspaper_data['summary'][:1000] if newspaper_data['summary'] else getattr(entry, 'summary', '')[:1000],
                "content": newspaper_data['text'][:5000] if newspaper_data['text'] else '',  # Limit content length
                "author": ', '.join(newspaper_data['authors'][:2]) if newspaper_data['authors'] else getattr(entry, 'author', None),
                "published_parsed": getattr(entry, 'published_parsed', None),  # Use RSS date as primary
                "newspaper_date": newspaper_data['publish_date'],  # Keep newspaper3k date as backup
                "updated_parsed": getattr(entry, 'updated_parsed', None),
                "categories": ','.join([tag.term for tag in getattr(entry, 'tags', [])]) or None,
                "source_feed": feed_url,
                "guid": getattr(entry, 'id', link),
                "language": getattr(entry, 'language', None),
                "thumbnail_url": newspaper_data['top_image'][:1000] if newspaper_data['top_image'] else None,
                "keywords": ', '.join(newspaper_data['keywords'][:10]) if newspaper_data['keywords'] else None
            })
        
        #print(f"  📊 Successfully processed {len(articles)} articles from this feed")
        return articles
        
    except Exception as e:
        print(f"  ❌ Error parsing feed {feed_url}: {e}")
        return []

def save_articles_to_db(articles):
    """Save all articles to database with enhanced metadata"""
    print(f"💾 Saving {len(articles)} articles to database...")
    
    # First, clean the table completely
    truncate_articles()
    
    app = create_app()
    with app.app_context():
        session = get_db_session()
        saved_count = 0
        
        try:
            for article_data in articles:
                # Parse dates
                published_date = None
                if article_data["published_parsed"]:
                    try:
                        published_date = datetime(*article_data["published_parsed"][:6])
                    except (TypeError, ValueError):
                        pass
                
                # Fallback to newspaper3k date
                if not published_date and article_data.get("newspaper_date"):
                    published_date = article_data["newspaper_date"]
                
                updated_date = None
                if article_data["updated_parsed"]:
                    try:
                        updated_date = datetime(*article_data["updated_parsed"][:6])
                    except (TypeError, ValueError):
                        pass
                
                # Create enhanced article object
                article = ArticleModel(
                    title=article_data["title"][:500],
                    link=article_data["link"][:200],
                    summary=article_data["summary"],  # Clean text from newspaper3k
                    content=article_data["content"],  # Clean full text from newspaper3k
                    author=article_data["author"][:200] if article_data["author"] else None,
                    published=published_date or datetime.utcnow(),
                    updated=updated_date,
                    categories=article_data["categories"][:100] if article_data["categories"] else None,
                    thumbnail_url=article_data["thumbnail_url"][:200] if article_data["thumbnail_url"] else None
                )
                
                session.merge(article)
                saved_count += 1
            
            # Commit all articles at once
            session.commit()
            print(f"🎉 Successfully saved {saved_count} articles with enhanced metadata!")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error saving articles to database: {e}")
            
        finally:
            session.close()

def main1():
    """Main execution function"""
    
    # Get RSS feeds from database
    feeds = get_rss_feeds()
    
    if not feeds:
        print("❌ No RSS feeds found in database 'rss' table!")
        return
    
    # Fetch articles from all feeds
    all_articles = []
    for (url,) in feeds:
        articles = fetch_articles_from_feed(url)
        all_articles.extend(articles)
    
    print(f"\n📊 Total articles processed: {len(all_articles)}")
    
    if all_articles:
        save_articles_to_db(all_articles)
    else:
        print("⚠️ No articles to save.")
    
    print("✨ Enhanced article fetch completed!")

if __name__ == "__main__":
    main1()

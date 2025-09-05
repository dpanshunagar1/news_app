from sqlalchemy import Column, Integer, String, Text, DateTime
from app import Base
from datetime import datetime

class Article(Base):
    """Enhanced Article model with rich RSS data"""
    __tablename__ = 'articles'
    
    # Primary fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    link = Column(String(1000), unique=True, nullable=False)
    
    # Content fields  
    summary = Column(Text)                    # RSS description/summary
    content = Column(Text)                    # Full content if available
    
    # Metadata fields
    author = Column(String(200))              # Author name
    published = Column(DateTime)              # Publication date
    updated = Column(DateTime)                # Last updated date
    
    # Organization fields
    categories = Column(String(500))          # Comma-separated tags/categories
    source_feed = Column(String(200))         # Which RSS feed this came from
    
    # Technical fields
    guid = Column(String(500))                # Unique RSS identifier
    language = Column(String(10))             # Content language (e.g., 'en')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Media (optional)
    thumbnail_url = Column(String(1000))      # Article image if available
    
    def __repr__(self):
        return f'<Article {self.title[:50]}...>'
    
    def to_dict(self):
        """Convert article to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'summary': self.summary,
            'content': self.content,
            'author': self.author,
            'published': self.published.isoformat() if self.published else None,
            'updated': self.updated.isoformat() if self.updated else None,
            'categories': self.categories,
            'source_feed': self.source_feed,
            'guid': self.guid,
            'language': self.language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'thumbnail_url': self.thumbnail_url
        }

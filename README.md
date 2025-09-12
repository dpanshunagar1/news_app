# 📰 News Aggregator

A modern Flask-based RSS news aggregator that fetches, processes, and displays articles from multiple RSS feeds with enhanced content extraction capabilities.

## 🚀 Features

- **RSS Feed Processing**: Automatically fetches articles from multiple RSS feeds
- **Enhanced Content Extraction**: Uses `newspaper3k` for clean text extraction, images, and metadata
- **Web Dashboard**: Browse articles with filtering and pagination
- **JSON API**: RESTful API endpoints for external integrations
- **Automated Scheduling**: Cron endpoint for scheduled article updates
- **Rich Metadata**: Authors, categories, publication dates, thumbnails
- **Content Quality Assessment**: Automatic rating of article content quality

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Content Processing**: feedparser, newspaper3k, BeautifulSoup
- **Database**: PostgreSQL (Supabase compatible)
- **Deployment**: Gunicorn, Railway ready
- **Environment**: Python 3.10+

## 📁 Project Structure

```
news-aggregator/
├── app/                    # Flask application package
│   ├── __init__.py        # App factory and database setup
│   ├── config.py          # Configuration management
│   ├── models.py          # SQLAlchemy models
│   ├── routes.py          # Web routes and API endpoints
│   ├── templates/         # Jinja2 templates
│   └── static/           # CSS, JS, images
├── article_extractor.py   # Enhanced article content extraction
├── database.py           # Database utility functions
├── fetch.py              # RSS fetching and processing
├── wsgi.py              # WSGI entry point
├── run.py               # Development server
├── requirements.txt     # Python dependencies
├── render.yaml         # Render deployment config
└── .env.example        # Environment variables template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd news-aggregator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # Create your PostgreSQL database
   # Update DATABASE_URL in .env
   python -c "from app import create_app; create_app()"
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

Visit `https://web-production-3df2.up.railway.app/` to view the application.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database

# RSS Feed URLs (comma-separated)
RSS_FEEDS=https://rss.cnn.com/rss/edition.rss,https://feeds.bbci.co.uk/news/rss.xml

# Cron Secret for scheduled tasks
CRON_SECRET=your-cron-secret-here

```


## 🔄 Article Fetching Process

1. **RSS Parsing**: Fetches RSS feeds from database
2. **Content Enhancement**: Uses newspaper3k for clean text extraction
3. **Data Processing**: Combines RSS metadata with extracted content
4. **Quality Assessment**: Rates content quality automatically
5. **Database Storage**: Saves processed articles with rich metadata


## 📈 Features in Detail

### Enhanced Content Extraction
- Clean text extraction without HTML
- Author identification and formatting
- Publication date parsing
- Image and media extraction
- Keyword and summary generation
- Content quality assessment

### Web Interface
- Responsive design
- Article filtering by author/category
- Pagination support
- Individual article pages
- Error handling

### API Features
- JSON responses
- Pagination metadata
- Filter support
- Error handling





## 🙏 Acknowledgments

- [newspaper3k](https://github.com/codelucas/newspaper) for content extraction
- [feedparser](https://github.com/kurtmckee/feedparser) for RSS parsing
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM

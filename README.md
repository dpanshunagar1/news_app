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
- **Deployment**: Gunicorn, Render/Railway ready
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

Visit `http://127.0.0.1:5000` to view the application.

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

### RSS Feeds Setup

1. Add RSS feed URLs to your database `rss` table:
   ```sql
   CREATE TABLE rss (
       id SERIAL PRIMARY KEY,
       url TEXT NOT NULL
   );
   
   INSERT INTO rss (url) VALUES 
   ('https://rss.cnn.com/rss/edition.rss'),
   ('https://feeds.bbci.co.uk/news/rss.xml'),
   ('https://www.reuters.com/rssFeed/topNews');
   ```

## 📡 API Endpoints

### Articles API
- `GET /api/articles` - Get paginated articles with filtering
- `GET /api/articles?page=2&author=John&category=tech` - Filtered results

### Cron Endpoint
- `POST /cron/fetch/?token=YOUR_CRON_SECRET` - Trigger article fetch

### Web Interface
- `GET /` - Homepage with article listing
- `GET /article/<id>` - Individual article view

## 🔄 Article Fetching Process

1. **RSS Parsing**: Fetches RSS feeds from database
2. **Content Enhancement**: Uses newspaper3k for clean text extraction
3. **Data Processing**: Combines RSS metadata with extracted content
4. **Quality Assessment**: Rates content quality automatically
5. **Database Storage**: Saves processed articles with rich metadata

## 🚀 Deployment

### Render Deployment

1. **Push to GitHub** (ensure `.env` is in `.gitignore`)

2. **Connect to Render** using the included `render.yaml`

3. **Set Environment Variables** in Render dashboard:
   - `FLASK_SECRET_KEY`
   - `DATABASE_URL`
   - `RSS_FEEDS`
   - `CRON_SECRET`

4. **Deploy** - Render will automatically build and deploy

### Manual Deployment

```bash
# Production server with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

## 📊 Database Schema

### Articles Table
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    link VARCHAR(1000) UNIQUE NOT NULL,
    summary TEXT,
    content TEXT,
    author VARCHAR(200),
    published TIMESTAMP,
    updated TIMESTAMP,
    categories VARCHAR(500),
    thumbnail_url VARCHAR(1000),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### RSS Feeds Table
```sql
CREATE TABLE rss (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL
);
```

## 🔧 Development

### Running Tests
```bash
# Add your test commands here
python -m pytest
```

### Code Formatting
```bash
# Format code with black
black .

# Sort imports
isort .
```

### Adding New RSS Feeds
```python
from database import get_db_connection

conn = get_db_connection()
cur = conn.cursor()
cur.execute("INSERT INTO rss (url) VALUES (%s)", ("https://new-feed-url.com/rss",))
conn.commit()
```

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check `DATABASE_URL` format
   - Ensure database is accessible
   - Verify credentials

2. **RSS Feed Parsing Issues**
   - Check feed URLs are valid
   - Some feeds may have parsing restrictions
   - Monitor logs for specific errors

3. **Content Extraction Failures**
   - newspaper3k may fail on some sites
   - Fallback to RSS content is automatic
   - Check site accessibility

### Logs
```bash
# View application logs
tail -f logs/app.log

# Database query logs
tail -f logs/db.log
```

## 📞 Support

For support, email your-email@example.com or create an issue on GitHub.

## 🙏 Acknowledgments

- [newspaper3k](https://github.com/codelucas/newspaper) for content extraction
- [feedparser](https://github.com/kurtmckee/feedparser) for RSS parsing
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
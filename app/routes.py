from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import desc, func, text
from app import get_db_session
from app.models import Article
from app.config import Config
from fetch import main1
import os


main = Blueprint('main', __name__)

def get_count_efficient(session, model):
    """Efficiently count rows without subqueries"""
    return session.query(func.count(model.id)).scalar()

@main.route('/')
def index():
    """Homepage with paginated articles showing enhanced data"""
    page = request.args.get('page', 1, type=int)
    per_page = Config.ARTICLES_PER_PAGE
    
    # Get filter parameters
    author_filter = request.args.get('author', '').strip()
    category_filter = request.args.get('category', '').strip()
    # source_filter = request.args.get('source', '').strip()
    
    # Calculate offset for pagination
    offset = (page - 1) * per_page
    
    # Get database session
    session = get_db_session()
    
    try:
        # Build query with filters
        query = session.query(Article)
        
        if author_filter:
            query = query.filter(Article.author.ilike(f'%{author_filter}%'))
        
        if category_filter:
            query = query.filter(Article.categories.ilike(f'%{category_filter}%'))
            
        # if source_filter:
        #     query = query.filter(Article.source_feed.ilike(f'%{source_filter}%'))
        
        # Get total count efficiently
        total_articles = query.count()
        
        # Get articles for current page with enhanced data
        articles = query.order_by(desc(Article.published))\
            .offset(offset)\
            .limit(per_page)\
            .all()
        
        # Get unique authors, sources for filter dropdowns
        authors = session.query(Article.author)\
            .filter(Article.author.isnot(None))\
            .distinct().all()
        
        # sources = session.query(Article.source_feed)\
        #     .filter(Article.source_feed.isnot(None))\
        #     .distinct().limit(10).all()
        
        # Calculate pagination info
        has_prev = page > 1
        has_next = offset + per_page < total_articles
        prev_page = page - 1 if has_prev else None
        next_page = page + 1 if has_next else None
        
        return render_template('index.html',
                             articles=articles,
                             has_prev=has_prev,
                             has_next=has_next,
                             prev_page=prev_page,
                             next_page=next_page,
                             current_page=page,
                             total_articles=total_articles,
                             authors=[a[0] for a in authors],
                            #  sources=[s[0] for s in sources],
                             current_author=author_filter,
                             current_category=category_filter
                            #  current_source=source_filter)
        )
    
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return render_template('index.html', articles=[], error="Error loading articles")
    
    finally:
        session.close()

@main.route('/api/articles')
def api_articles():
    """JSON API endpoint for articles with enhanced metadata"""
    page = request.args.get('page', 1, type=int)
    per_page = Config.ARTICLES_PER_PAGE
    
    # Get filter parameters
    author_filter = request.args.get('author', '').strip()
    category_filter = request.args.get('category', '').strip()
    # source_filter = request.args.get('source', '').strip()
    
    # Calculate offset for pagination
    offset = (page - 1) * per_page
    
    # Get database session
    session = get_db_session()
    
    try:
        # Build query with filters
        query = session.query(Article)
        
        if author_filter:
            query = query.filter(Article.author.ilike(f'%{author_filter}%'))
        
        if category_filter:
            query = query.filter(Article.categories.ilike(f'%{category_filter}%'))
            
        # if source_filter:
        #     query = query.filter(Article.source_feed.ilike(f'%{source_filter}%'))
        
        # Get total count efficiently
        total_articles = query.count()
        
        # Get articles for current page
        articles = query.order_by(desc(Article.published))\
            .offset(offset)\
            .limit(per_page)\
            .all()
        
        # Convert to dictionaries with enhanced fields
        articles_data = [article.to_dict() for article in articles]
        
        # Calculate pagination info
        has_prev = page > 1
        has_next = offset + per_page < total_articles
        
        return jsonify({
            'articles': articles_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_articles,
                'has_prev': has_prev,
                'has_next': has_next,
                'prev_page': page - 1 if has_prev else None,
                'next_page': page + 1 if has_next else None
            },
            'filters': {
                'author': author_filter,
                'category': category_filter
                # 'source': source_filter
            }
        })
    
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return jsonify({'error': 'Error loading articles'}), 500
    
    finally:
        session.close()

@main.route('/article/<int:article_id>')
def article_detail(article_id):
    """Individual article page showing full content"""
    session = get_db_session()
    
    try:
        article = session.query(Article).get(article_id)
        
        if not article:
            return render_template('error.html', 
                                 error="Article not found", 
                                 message="The requested article does not exist."), 404
        
        return render_template('article_detail.html', article=article)
    
    except Exception as e:
        print(f"Error fetching article {article_id}: {e}")
        return render_template('error.html', 
                             error="Error loading article", 
                             message="Please try again later."), 500
    
    finally:
        session.close()


# Here we define a route to trigger the fetch process manually

CRON_SECRET = os.getenv("CRON_SECRET", "changeme")

@main.route("/cron/fetch/", methods=["POST", "GET"])
def cron_fetch():
    token = request.args.get("token")
    if token != CRON_SECRET:
        return jsonify({"error": "Unauthorized"}), 403
    main1()
    return jsonify({"status": "success"})



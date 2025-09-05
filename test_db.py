from app import create_app, get_db_session
from app.models import Article

def test_connection():
    """Test database connection"""
    try:
        app = create_app()
        with app.app_context():
            session = get_db_session()
            
            # Try a simple count query
            count = session.execute("SELECT COUNT(*) FROM articles").scalar()
            print(f"✅ Database connection successful! Found {count} articles.")
            
            session.close()
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == '__main__':
    test_connection()

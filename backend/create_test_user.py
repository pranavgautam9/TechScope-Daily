"""
Script to create a test user in the database
Run this script once to create the test user: testuser@gmail.com
"""
from app.models.database import SessionLocal, User
from app.core.security import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "testuser@gmail.com").first()
        if existing_user:
            print("Test user already exists!")
            return
        
        # Create test user
        test_user = User(
            email="testuser@gmail.com",
            first_name="Test",
            last_name="User",
            hashed_password=get_password_hash("Password123!")
        )
        
        db.add(test_user)
        db.commit()
        print("Test user created successfully!")
        print(f"Email: testuser@gmail.com")
        print(f"Password: Password123!")
    except Exception as e:
        db.rollback()
        print(f"Error creating test user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()


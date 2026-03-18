"""
Script to create a test user in the database
Run this script once to create the test user: testuser@gmail.com
"""
from app.models.database import SessionLocal, User
from app.core.security import get_password_hash, verify_password
from sqlalchemy import func

def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(func.lower(User.email) == "testuser@gmail.com").first()
        if existing_user:
            # If the test user exists but the password differs, reset it.
            if not verify_password("Password123!", existing_user.hashed_password):
                existing_user.hashed_password = get_password_hash("Password123!")
                db.add(existing_user)
                db.commit()
                print("Test user existed but password mismatch; reset to Password123!")
            else:
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


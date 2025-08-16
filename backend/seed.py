from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from .db import engine, SessionLocal, Base
from .models import User, UserActivity

# Create tables if not exist
Base.metadata.create_all(bind=engine)

def seed():
    db: Session = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Seed: data already present; skipping.")
            return

        users = [
            User(email="alice@example.com", age=29, location="New York", signup_date=date(2023, 5, 10), last_login=datetime.utcnow(), job_industry="Tech"),
            User(email="bob@example.com", age=35, location="California", signup_date=date(2022, 11, 2), last_login=datetime.utcnow()-timedelta(days=3), job_industry="Finance"),
            User(email="carol@example.com", age=41, location="Ontario", signup_date=date(2024, 2, 14), last_login=datetime.utcnow()-timedelta(days=1), job_industry="Healthcare"),
            User(email="dave@example.com", age=31, location="California", signup_date=date(2021, 8, 23), last_login=datetime.utcnow()-timedelta(days=5), job_industry="Tech"),
        ]
        db.add_all(users)
        db.flush()

        activities = [
            UserActivity(user_id=users[0].id, activity_date=date.today()-timedelta(days=1), activity_type="login"),
            UserActivity(user_id=users[0].id, activity_date=date.today(), activity_type="purchase"),
            UserActivity(user_id=users[1].id, activity_date=date.today()-timedelta(days=2), activity_type="login"),
            UserActivity(user_id=users[2].id, activity_date=date.today()-timedelta(days=3), activity_type="login"),
            UserActivity(user_id=users[3].id, activity_date=date.today(), activity_type="logout"),
        ]
        db.add_all(activities)
        db.commit()
        print("Seed: inserted sample users and activities.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
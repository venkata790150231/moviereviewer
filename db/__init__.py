# Create a PostgreSQL database connection
import logging
import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = os.environ["DATABASE_URL"]
engine = create_engine(db_url)

# Create a base class for declarative models
Base = declarative_base()


# Define a model class
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    huff_title = Column(String)
    nypost_title = Column(String)
    daily_caller = Column(String)
    url = Column(String, unique=True)
    post = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create the database schema
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def publish(post: Post):
    session.add(post)
    session.commit()


def delete_post(identifier: int):
    logging.info("Deleting post with id: %s", identifier)
    instance = session.query(Post).get(identifier)
    session.delete(instance)
    session.commit()


def load() -> Post:
    return session.query(Post).all()

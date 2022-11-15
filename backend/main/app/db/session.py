""" SQLAlchemy session management. """

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connection_uri = settings.db.DATABASE_CONNECTION_URL
engine = create_engine(
    connection_uri,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

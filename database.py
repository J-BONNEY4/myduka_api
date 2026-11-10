
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL
DATABASE_URL = "sqlite:///./myduka_api.db"

# Connect sql to the engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create Base
Base = declarative_base()

# Create database session 
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# stores database session
session = SessionLocal()

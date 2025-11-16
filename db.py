from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/inventory"

# echo set to True will log all the SQL statements
# connect_args={"options": "-c timezone=utc"} to set timezone to UTC
# connect_args={"sslmode": "require"} to enforce SSL connection
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

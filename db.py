from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/inventory"

# echo set to True will log all the SQL statements
# connect_args={"options": "-c timezone=utc"} to set timezone to UTC
# connect_args={"sslmode": "require"} to enforce SSL connection
engine = create_engine(DATABASE_URL)

# autocommit is set to False to manage transactions manually
# flush is all updates to the database are not committed until explicitly flushed
# autoflush is set to False to prevent automatic flushing of changes
# bind=engine to bind the session to the engine that means
# the session will use this engine to connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

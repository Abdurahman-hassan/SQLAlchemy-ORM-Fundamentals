from db import engine
from models import Base


def reset_database():
    """
    Drops all tables and recreates them based on the current models.
    """
    # we didn't use session here because we are just dropping and creating tables
    # this is a schema level operation not a data level operation
    # because of that we use the engine directly
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

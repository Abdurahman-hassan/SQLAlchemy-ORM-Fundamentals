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



"""
In the function reset_database(), we don't use the get_session() function because this function is primarily focused on schema management rather than data manipulation.

Here are the steps explaining why:
1) Purpose of reset_database():
    - The primary goal of this function is to drop all existing tables and recreate them using the metadata defined in your SQLAlchemy models. This is usually part of initial setup or reset operations, not data transactions.

2) No Data Transactions:
    - Since reset_database() is only dealing with database schema (i.e., the structure of the tables) and not with actual data (inserts, updates, deletes), there's no need to establish a session or use get_session().

3) Schema Operations:
    - Operations like drop_all() and create_all() work at the database level and do not involve session-based operations.
    They directly interact with the database engine to modify the schema.

    4) Session Context:
    - As noted in the snippets, sessions are essential when you are performing data operations (like querying or modifying data) because they manage state and transactions. For schema operations, this isn't required.

In conclusion, use of sessions is primarily for data manipulation, whereas schema operations like those in reset_database() can directly utilize the database engine.
"""




"""

In SQLAlchemy, sessions are crucial for managing interactions with the database. Here's a breakdown of how to use sessions effectively in data operations:

1) Creating a Session:
Use the sessionmaker function to create a session factory. This factory can then be used to instantiate sessions.
    
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine)

2) Starting a Session:
To interact with the database, you create a session instance from your session factory.

    db = SessionLocal()

3) Performing Data Operations:
    You can use the session instance to add or make changes to your models. For example, adding a new object:

    new_item = MyModel(name="example")
    db.add(new_item)

4) Committing Changes:
    After making your modifications (inserts, updates, or deletes), you must explicitly commit these changes to persist them in the database.
    
    db.commit()

5) Closing the Session:
    Once you’re done working with the database, it's important to close the session to free up resources.
    
    db.close()

6) Using Context Managers:
    
    You can enhance session management by using a context manager to ensure that sessions are closed properly even if an error occurs. Here’s an example of how to implement it:

    from contextlib import contextmanager
    
    @contextmanager
    def session_scope():
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

7) Usage of Context Manager:

    With this context manager, you can use your session in a scope like this:
    
    with session_scope() as session:
        new_item = MyModel(name="example")
        session.add(new_item)

Using sessions effectively allows you to manage database transactions efficiently, handle errors gracefully, and ensure data integrity. 
"""
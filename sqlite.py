from sqlalchemy import create_engine, text, String, select
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///example.db")

with Session(engine) as session:
    # Create a table
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT
        )
    """))
    
    # Insert simple data
    session.execute(text("INSERT INTO users (name, role) VALUES ('Alice', 'Admin')"))
    
    # Commit changes
    session.commit()
# Ready to start coding!

with Session(engine) as session:
    # Safe execution with parameters
    stmt = text("INSERT INTO users (name, role) VALUES (:name, :role)")
    params = {"name": "Bob", "role": "User"}

    session.execute(stmt, params)
    session.commit()


with Session(engine) as session:
    result = session.execute(text("SELECT * FROM users"))
    print(result.fetchall().asdict())


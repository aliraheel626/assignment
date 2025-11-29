from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
# 1. Setup the database connection
# We use an in-memory database for this tutorial so it's fresh every time, 
# or a file-based one. Let's stick to the file as per original.
engine = create_engine("sqlite:///example.db", echo=False)

print("--- STARTING SQLITE CRUD TUTORIAL ---\n")

# --- 1. SETUP & RESET ---
# We drop the table first to ensure we start with a clean slate every time we run this script.
with engine.connect() as connection:
    print("1. [SETUP] Resetting database...")
    connection.execute(text("DROP TABLE IF EXISTS users"))
    connection.execute(text("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT
        )
    """))
    connection.commit()
    print("   -> Table 'users' created.")

# --- 2. CREATE (Insert) --- POST
# We insert multiple records using parameter binding for security.
with Session(engine) as session:
    print("\n2. [CREATE] Inserting new users...")
    data = [
        {"name": "Alice", "role": "Admin"},
        {"name": "Bob", "role": "User"},
        {"name": "Charlie", "role": "User"},
        {"name": "Diana", "role": "Guest"}
    ]
    session.execute(
        text("INSERT INTO users (name, role) VALUES (:name, :role)"),
        data
    )
    session.commit()
    print(f"   -> Inserted {len(data)} users: {', '.join(d['name'] for d in data)}")

# --- 3. READ (Select) --- GET
# We query for users with the role 'User'.
with Session(engine) as session:
    print("\n3. [READ] Querying users with role 'User'...")
    result = session.execute(
        text("SELECT * FROM users WHERE role=:role"), 
        {"role": "User"}
    )
    
    rows = result.fetchall()
    if rows:
        for row in rows:
            print(f"   -> Found: {row.name} (Role: {row.role})")
    else:
        print("   -> No users found.")

# --- 4. UPDATE ---
# We update 'Bob' to be a 'SuperUser'.
with Session(engine) as session:
    print("\n4. [UPDATE] Promoting 'Bob' to 'SuperUser'...")
    session.execute(
        text("UPDATE users SET role=:new_role WHERE name=:name"),
        {"new_role": "SuperUser", "name": "Bob"}
    )
    session.commit()
    print("   -> Update committed.")

# --- 5. DELETE ---
# We delete 'Charlie' from the database.
with Session(engine) as session:
    print("\n5. [DELETE] Removing user 'Charlie'...")
    session.execute(
        text("DELETE FROM users WHERE name=:name"),
        {"name": "Charlie"}
    )
    session.commit()
    print("   -> Delete committed.")

# --- 6. VERIFY ---
# Check the final state of the database.
with Session(engine) as session:
    print("\n6. [VERIFY] Final list of users:")
    result = session.execute(text("SELECT * FROM users ORDER BY id"))
    for row in result:
        # row._asdict() converts the row to a dictionary for easy printing
        print(f"   -> {row._asdict()}")



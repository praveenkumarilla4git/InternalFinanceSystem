import sqlite3

connection = sqlite3.connect("finance.db")
cursor = connection.cursor()

# We added 'reason TEXT' to the list below
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        monthly_savings INTEGER,
        projected_annual INTEGER,
        reason TEXT
    );
    """
)

connection.commit()
connection.close()
print("New Database structure (with Reason) created!")
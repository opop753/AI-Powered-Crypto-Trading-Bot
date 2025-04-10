import sqlite3

# Connect to the new_test.db database
conn = sqlite3.connect('new_test.db')
cursor = conn.cursor()

# Execute a query to get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the list of tables
print("Tables in the database:", tables)

# Close the connection
conn.close()

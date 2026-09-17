# Security Doctor SQL Injection Demo
import sqlite3

def find_user(user_input):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL Injection Vulnerability
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    cursor.execute(query)
    return cursor.fetchall()

import sqlite3

# Connect to DB
conn = sqlite3.connect("database/facemash.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS facemash_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT NOT NULL,
    rating INTEGER DEFAULT 1200
)
''')

# Preload images
import os
images = [img for img in os.listdir("static/images")]

for img in images:
    cursor.execute("INSERT INTO facemash_images (image_name) VALUES (?)", (img,))

conn.commit()
conn.close()
print("Database created and images preloaded!")

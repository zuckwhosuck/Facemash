from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from elo import calculate_elo
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Connect to DB
def connect_db():
    conn = sqlite3.connect("database/facemash.db")
    return conn

# Load homepage with 2 random images
@app.route("/")
def index():
    conn = connect_db()
    cursor = conn.cursor()

    if 'images' not in session:
        cursor.execute("SELECT id, image_name, rating FROM facemash_images ORDER BY RANDOM() LIMIT 2")
        images = cursor.fetchall()
        session['images'] = images
    else:
        images = session['images']

    conn.close()
    return render_template("index.html", images=images)

# Handle voting
@app.route("/vote", methods=["POST"])
def vote():
    winner_id = request.form["winner"]
    loser_id = request.form["loser"]

    conn = connect_db()
    cursor = conn.cursor()

    # Get ratings
    cursor.execute("SELECT rating FROM facemash_images WHERE id=?", (winner_id,))
    winner_rating = cursor.fetchone()[0]
    cursor.execute("SELECT rating FROM facemash_images WHERE id=?", (loser_id,))
    loser_rating = cursor.fetchone()[0]

    # Update Elo ratings
    new_winner_rating, new_loser_rating = calculate_elo(winner_rating, loser_rating)

    # Update DB
    cursor.execute("UPDATE facemash_images SET rating=? WHERE id=?", (new_winner_rating, winner_id))
    cursor.execute("UPDATE facemash_images SET rating=? WHERE id=?", (new_loser_rating, loser_id))
    conn.commit()

    # Get new random images
    cursor.execute("SELECT id, image_name, rating FROM facemash_images ORDER BY RANDOM() LIMIT 2")
    images = cursor.fetchall()
    session['images'] = images

    conn.close()

    return redirect(url_for("index"))

# Leaderboard
@app.route("/leaderboard")
def leaderboard():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT image_name, rating FROM facemash_images ORDER BY rating DESC LIMIT 10")
    images = cursor.fetchall()
    conn.close()
    return render_template("leaderboard.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)

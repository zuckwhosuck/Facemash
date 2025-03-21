# Elo Rating System for Facemash

def calculate_elo(winner_rating, loser_rating, k=32):
    expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_rating - loser_rating) / 400))

    new_winner_rating = winner_rating + k * (1 - expected_winner)
    new_loser_rating = loser_rating + k * (0 - expected_loser)

    return round(new_winner_rating), round(new_loser_rating)
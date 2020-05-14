import sqlite3


def get_connection():
    conn = sqlite3.connect('../recomendations.db')
    return conn

import os
import random
import sqlite3
import sys
from models.Score import Score


class Database:
    db_name = "databases/hangman_2025.db"
    table_leaderboard = "leaderboard"
    table_words = "words"

    def __init__(self):
        if not os.path.exists(self.db_name):
            raise FileNotFoundError('Andmebaasi ei leitud')

        """Konstruktor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = None
        self.connect()  # Loo ühendus
        self.cursor = self.conn.cursor()

        #self.word, self.category = self.get_random_word()
        #self.hidden_word = ["_"] * len(self.word)
        #self.guessed_letters = set()
        self.check_if_table_leaderboard_exists()
        self.check_if_table_words_exists()
        self.read_leaderboard()
        self.get_categories()
        self.get_random_word()


    def connect(self):
        """Loob ühenduse andmebaasiga"""
        try:
            if self.conn:
                self.conn.close()  # eelnev ühendus suletakse
                print('Varasem andmebaasi ühendus suleti')
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Uus ühendus andmebaasiga {self.db_name} loodud')
        except sqlite3.Error as error:
            print(f'Tõrge andmebaasi ühenduse loomisel:{error}')
            self.conn = None
            self.cursor = None

    def check_if_table_words_exists(self):
        self.cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (self.table_words,))
        result = self.cursor.fetchone()
        if result:
            print(f"Tabel '{self.table_words}' on olemas.")
        else:
            print(f"Tabelit '{self.table_words}' andmebaasist ei leitud. Programm lõpetab töö.")
            sys.exit(1)

    def check_if_table_leaderboard_exists(self):
        self.cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (self.table_leaderboard,))
        result = self.cursor.fetchone()
        if result:
            print(f"Tabel '{self.table_leaderboard}' on olemas.")
        else:
            self.create_table()
            print(f"Tabelit '{self.table_leaderboard}' andmebaasist ei leitud. Luuakse uus edetabel")

    def create_table(self):
        # Kui tabel leaderboard puudub
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id NOT NULL INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                word TEXT NOT NULL,
                letters TEXT,
                game_length INTEGER NOT NULL,
                game_time TEXT NOT NULL
            )
        ''')
        print(f'Loodi tabel: {self.table_leaderboard}.')
        self.conn.commit()


    def get_random_word(self, category=None):
        #print(f'Kas jõuab siia see info: {category}')
        if category is None:
            self.cursor.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1")
            word = self.cursor.fetchone()
            for word in word:
                #print(f'Sõna: {word}')
                return word
        elif category.lower():
            cat = category.lower()
            #print(cat)
            self.cursor.execute("SELECT word FROM words where category=? ORDER BY RANDOM() LIMIT 1", (cat, ))
            word = self.cursor.fetchone()
            for word in word:
                #print(f'Nüüd selline {word}')
                return word
        """elif category.lower() == 'sõiduk':
            self.cursor.execute("SELECT word FROM words where category=? ORDER BY RANDOM() LIMIT 1", ('sõiduk',))
            word = self.cursor.fetchone()
            for word in word:
                print(f'Õige sõna: {word}')
                return word"""

    def get_categories(self):
        self.cursor.execute("SELECT DISTINCT category FROM words")
        data = self.cursor.fetchall()
        categories = [category[0] for category in data]
        categories.sort()
        categories.insert(0, 'Vali kategooria')
        #print(f'Kategooriad: {categories}.')
        return [category.capitalize() for category in categories]

    def close(self):
        self.conn.close()

    def read_leaderboard(self):
        self.cursor.execute("select * from leaderboard")
        result = self.cursor.fetchall()
        return result








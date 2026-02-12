import sqlite3
from datetime import datetime, timedelta
import json

DATABASE_NAME = 'flashcards.db'

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Decks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cards table with SM-2 algorithm fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            easiness_factor REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 0,
            repetitions INTEGER DEFAULT 0,
            next_review TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
        )
    ''')
    
    # Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            api_provider TEXT DEFAULT 'groq',
            api_key TEXT,
            hotkey_again TEXT DEFAULT 'ctrl+1',
            hotkey_hard TEXT DEFAULT 'ctrl+2',
            hotkey_good TEXT DEFAULT 'ctrl+3',
            hotkey_easy TEXT DEFAULT 'ctrl+4'
        )
    ''')
    
    # Insert default settings if not exists
    cursor.execute('SELECT COUNT(*) FROM settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO settings (id, api_provider, api_key, hotkey_again, hotkey_hard, hotkey_good, hotkey_easy)
            VALUES (1, 'groq', '', 'ctrl+1', 'ctrl+2', 'ctrl+3', 'ctrl+4')
        ''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Deck operations
def create_deck(name):
    """Create a new deck"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO decks (name) VALUES (?)', (name,))
        deck_id = cursor.lastrowid
        conn.commit()
        return deck_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_all_decks():
    """Get all decks with card counts"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.id, d.name, d.created_at, COUNT(c.id) as card_count,
               SUM(CASE WHEN c.next_review <= datetime('now') THEN 1 ELSE 0 END) as due_count
        FROM decks d
        LEFT JOIN cards c ON d.id = c.deck_id
        GROUP BY d.id
        ORDER BY d.created_at DESC
    ''')
    decks = cursor.fetchall()
    conn.close()
    return decks

def get_deck_by_id(deck_id):
    """Get deck by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM decks WHERE id = ?', (deck_id,))
    deck = cursor.fetchone()
    conn.close()
    return deck

def delete_deck(deck_id):
    """Delete a deck and all its cards"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM decks WHERE id = ?', (deck_id,))
    conn.commit()
    conn.close()

# Card operations
def add_card(deck_id, question, answer):
    """Add a new card to a deck"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cards (deck_id, question, answer)
        VALUES (?, ?, ?)
    ''', (deck_id, question, answer))
    card_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return card_id

def add_cards_bulk(deck_id, cards_list):
    """Add multiple cards to a deck"""
    conn = get_connection()
    cursor = conn.cursor()
    for card in cards_list:
        cursor.execute('''
            INSERT INTO cards (deck_id, question, answer)
            VALUES (?, ?, ?)
        ''', (deck_id, card['question'], card['answer']))
    conn.commit()
    conn.close()

def get_cards_by_deck(deck_id):
    """Get all cards in a deck"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cards WHERE deck_id = ?
        ORDER BY created_at DESC
    ''', (deck_id,))
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_due_cards(deck_id):
    """Get cards that are due for review"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM cards
        WHERE deck_id = ? AND next_review <= datetime('now')
        ORDER BY next_review ASC
    ''', (deck_id,))
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_card_by_id(card_id):
    """Get a card by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cards WHERE id = ?', (card_id,))
    card = cursor.fetchone()
    conn.close()
    return card

def update_card(card_id, question, answer):
    """Update a card's question and answer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cards SET question = ?, answer = ?
        WHERE id = ?
    ''', (question, answer, card_id))
    conn.commit()
    conn.close()

def delete_card(card_id):
    """Delete a card"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()

def update_card_review(card_id, easiness_factor, interval, repetitions, next_review):
    """Update card's SM-2 parameters after review"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cards
        SET easiness_factor = ?, interval = ?, repetitions = ?, next_review = ?
        WHERE id = ?
    ''', (easiness_factor, interval, repetitions, next_review, card_id))
    conn.commit()
    conn.close()

# Settings operations
def get_settings():
    """Get application settings"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE id = 1')
    settings = cursor.fetchone()
    conn.close()
    return settings

def update_settings(api_provider, api_key, hotkey_again, hotkey_hard, hotkey_good, hotkey_easy):
    """Update application settings"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE settings
        SET api_provider = ?, api_key = ?, hotkey_again = ?, hotkey_hard = ?, hotkey_good = ?, hotkey_easy = ?
        WHERE id = 1
    ''', (api_provider, api_key, hotkey_again, hotkey_hard, hotkey_good, hotkey_easy))
    conn.commit()
    conn.close()
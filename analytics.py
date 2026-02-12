"""
Analytics module with NumPy for numerical operations
"""

import database as db
from datetime import datetime, timedelta
import numpy as np

def get_study_statistics(deck_id=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if deck_id:
        cursor.execute('''
            SELECT 
                COUNT(*) as total_cards,
                SUM(CASE WHEN repetitions > 0 THEN 1 ELSE 0 END) as studied_cards,
                AVG(easiness_factor) as avg_easiness,
                SUM(CASE WHEN next_review <= datetime('now') THEN 1 ELSE 0 END) as due_cards,
                AVG(interval) as avg_interval,
                SUM(repetitions) as total_reviews
            FROM cards
            WHERE deck_id = ?
        ''', (deck_id,))
    else:
        cursor.execute('''
            SELECT 
                COUNT(*) as total_cards,
                SUM(CASE WHEN repetitions > 0 THEN 1 ELSE 0 END) as studied_cards,
                AVG(easiness_factor) as avg_easiness,
                SUM(CASE WHEN next_review <= datetime('now') THEN 1 ELSE 0 END) as due_cards,
                AVG(interval) as avg_interval,
                SUM(repetitions) as total_reviews
            FROM cards
        ''')
    
    result = cursor.fetchone()
    conn.close()
    
    total_cards = result['total_cards'] or 0
    studied_cards = result['studied_cards'] or 0
    
    return {
        'total_cards': total_cards,
        'studied_cards': studied_cards,
        'unstudied_cards': total_cards - studied_cards,
        'due_cards': result['due_cards'] or 0,
        'avg_easiness': round(result['avg_easiness'] or 2.5, 2),
        'avg_interval': round(result['avg_interval'] or 0, 1),
        'total_reviews': result['total_reviews'] or 0,
        'retention_rate': round((studied_cards / total_cards * 100) if total_cards > 0 else 0, 1)
    }

def get_numerical_statistics(deck_id=None):
    """Uses NumPy for advanced numerical operations"""
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if deck_id:
        cursor.execute('SELECT easiness_factor, interval, repetitions FROM cards WHERE deck_id = ? AND repetitions > 0', (deck_id,))
    else:
        cursor.execute('SELECT easiness_factor, interval, repetitions FROM cards WHERE repetitions > 0')
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return {
            'ef_mean': 2.5, 'ef_std': 0.0, 'ef_median': 2.5,
            'ef_25th': 2.5, 'ef_75th': 2.5,
            'interval_mean': 0.0, 'interval_std': 0.0,
            'reps_mean': 0.0, 'reps_std': 0.0
        }
    
    # NumPy arrays for numerical operations
    easiness_factors = np.array([row['easiness_factor'] for row in results])
    intervals = np.array([row['interval'] for row in results])
    repetitions = np.array([row['repetitions'] for row in results])
    
    # NumPy numerical operations
    return {
        'ef_mean': round(float(np.mean(easiness_factors)), 2),
        'ef_std': round(float(np.std(easiness_factors)), 2),
        'ef_median': round(float(np.median(easiness_factors)), 2),
        'ef_25th': round(float(np.percentile(easiness_factors, 25)), 2),
        'ef_75th': round(float(np.percentile(easiness_factors, 75)), 2),
        'interval_mean': round(float(np.mean(intervals)), 1),
        'interval_std': round(float(np.std(intervals)), 1),
        'reps_mean': round(float(np.mean(repetitions)), 1),
        'reps_std': round(float(np.std(repetitions)), 1)
    }

def calculate_correlation_matrix():
    """Calculate correlations using NumPy"""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT easiness_factor, interval, repetitions FROM cards WHERE repetitions > 0')
    results = cursor.fetchall()
    conn.close()
    
    if len(results) < 3:
        return {'ef_interval': 0.0, 'ef_reps': 0.0, 'interval_reps': 0.0}
    
    ef = np.array([row['easiness_factor'] for row in results])
    intervals = np.array([row['interval'] for row in results])
    reps = np.array([row['repetitions'] for row in results])
    
    data_matrix = np.array([ef, intervals, reps])
    correlation_matrix = np.corrcoef(data_matrix)
    
    return {
        'ef_interval': round(float(correlation_matrix[0, 1]), 3),
        'ef_reps': round(float(correlation_matrix[0, 2]), 3),
        'interval_reps': round(float(correlation_matrix[1, 2]), 3)
    }

# Keep original functions
def get_deck_statistics():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.id, d.name, COUNT(c.id) as total_cards,
               SUM(CASE WHEN c.repetitions > 0 THEN 1 ELSE 0 END) as studied,
               SUM(CASE WHEN c.next_review <= datetime('now') THEN 1 ELSE 0 END) as due,
               AVG(c.easiness_factor) as avg_ef,
               SUM(c.repetitions) as total_reviews
        FROM decks d
        LEFT JOIN cards c ON d.id = c.deck_id
        GROUP BY d.id ORDER BY d.name
    ''')
    
    decks = []
    for row in cursor.fetchall():
        total = row['total_cards'] or 0
        studied = row['studied'] or 0
        decks.append({
            'id': row['id'],
            'name': row['name'],
            'total_cards': total,
            'studied_cards': studied,
            'due_cards': row['due'] or 0,
            'avg_easiness': round(row['avg_ef'] or 2.5, 2),
            'total_reviews': row['total_reviews'] or 0,
            'progress': round((studied / total * 100) if total > 0 else 0, 1)
        })
    conn.close()
    return decks

def get_interval_distribution(deck_id=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    query = '''
        SELECT 
            CASE 
                WHEN interval = 0 THEN 'New'
                WHEN interval = 1 THEN '1 day'
                WHEN interval <= 7 THEN '2-7 days'
                WHEN interval <= 30 THEN '1-4 weeks'
                WHEN interval <= 90 THEN '1-3 months'
                ELSE '3+ months'
            END as interval_group,
            COUNT(*) as count
        FROM cards
        {} GROUP BY interval_group
    '''.format('WHERE deck_id = ?' if deck_id else '')
    
    cursor.execute(query, (deck_id,) if deck_id else ())
    results = cursor.fetchall()
    conn.close()
    return {
        'labels': [row['interval_group'] for row in results],
        'values': [row['count'] for row in results]
    }

def get_easiness_distribution(deck_id=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    query = '''
        SELECT 
            CASE 
                WHEN easiness_factor < 1.8 THEN 'Very Hard'
                WHEN easiness_factor < 2.2 THEN 'Hard'
                WHEN easiness_factor < 2.8 THEN 'Medium'
                ELSE 'Easy'
            END as difficulty,
            COUNT(*) as count
        FROM cards
        WHERE repetitions > 0 {}
        GROUP BY difficulty
    '''.format('AND deck_id = ?' if deck_id else '')
    
    cursor.execute(query, (deck_id,) if deck_id else ())
    results = cursor.fetchall()
    conn.close()
    return {
        'labels': [row['difficulty'] for row in results],
        'values': [row['count'] for row in results]
    }

def get_upcoming_reviews(days=7):
    conn = db.get_connection()
    cursor = conn.cursor()
    data = {'labels': [], 'values': []}
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        cursor.execute('SELECT COUNT(*) as count FROM cards WHERE DATE(next_review) = ?', 
                      (date.strftime('%Y-%m-%d'),))
        result = cursor.fetchone()
        data['labels'].append(date.strftime('%b %d'))
        data['values'].append(result['count'] or 0)
    conn.close()
    return data

def calculate_retention_metrics():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor = cursor.execute('SELECT COUNT(*) FROM cards WHERE repetitions >= 1')
    passed_first = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM cards WHERE repetitions >= 2')
    passed_second = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM cards WHERE repetitions >= 3')
    mature_cards = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM cards WHERE repetitions > 0')
    total_studied = cursor.fetchone()[0] or 1
    conn.close()
    
    return {
        'first_review_retention': round((passed_first / total_studied * 100), 1),
        'second_review_retention': round((passed_second / total_studied * 100), 1),
        'mature_card_rate': round((mature_cards / total_studied * 100), 1),
        'mature_cards': mature_cards,
        'total_studied': total_studied
    }

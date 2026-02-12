from datetime import datetime, timedelta

def calculate_next_review(quality, easiness_factor, interval, repetitions):
    """
    SM-2 Algorithm for spaced repetition
    
    Args:
        quality: 0 (Again), 1 (Hard), 2 (Good), 3 (Easy)
        easiness_factor: Current easiness factor (EF)
        interval: Current interval in days
        repetitions: Number of successful repetitions
    
    Returns:
        tuple: (new_easiness_factor, new_interval, new_repetitions, next_review_date)
    """
    
    # Update easiness factor
    new_ef = easiness_factor + (0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02))
    
    # Ensure EF stays within bounds (minimum 1.3)
    if new_ef < 1.3:
        new_ef = 1.3
    
    # Calculate new interval and repetitions
    if quality < 2:  # Again (0) or Hard (1)
        # Reset repetitions and start over
        new_repetitions = 0
        new_interval = 1
    else:
        # Good (2) or Easy (3)
        new_repetitions = repetitions + 1
        
        if new_repetitions == 1:
            new_interval = 1
        elif new_repetitions == 2:
            new_interval = 6
        else:
            new_interval = round(interval * new_ef)
        
        # Bonus interval for "Easy"
        if quality == 3:
            new_interval = round(new_interval * 1.3)
    
    # Calculate next review date
    next_review = datetime.now() + timedelta(days=new_interval)
    
    return (new_ef, new_interval, new_repetitions, next_review.strftime('%Y-%m-%d %H:%M:%S'))

def get_quality_from_rating(rating):
    """
    Convert rating string to quality number for SM-2
    
    Args:
        rating: 'again', 'hard', 'good', or 'easy'
    
    Returns:
        int: Quality (0-3)
    """
    rating_map = {
        'again': 0,
        'hard': 1,
        'good': 2,
        'easy': 3
    }
    return rating_map.get(rating.lower(), 2)
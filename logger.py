"""
Logging module for AI Flashcards application
Tracks user actions, errors, and system events
"""

import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Create logger
logger = logging.getLogger('flashcards_app')
logger.setLevel(logging.DEBUG)

# File handler - logs everything to file
log_filename = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Console handler - logs INFO and above to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Convenience functions
def log_info(message):
    """Log informational message"""
    logger.info(message)

def log_error(message, exception=None):
    """Log error message with optional exception"""
    if exception:
        logger.error(f"{message}: {str(exception)}", exc_info=True)
    else:
        logger.error(message)

def log_warning(message):
    """Log warning message"""
    logger.warning(message)

def log_debug(message):
    """Log debug message"""
    logger.debug(message)

# Specific domain loggers
def log_deck_created(deck_name, deck_id):
    """Log deck creation"""
    logger.info(f"DECK_CREATED - Name: {deck_name}, ID: {deck_id}")

def log_cards_generated(deck_id, count, provider):
    """Log card generation"""
    logger.info(f"CARDS_GENERATED - Deck ID: {deck_id}, Count: {count}, Provider: {provider}")

def log_study_session_started(deck_id, card_count):
    """Log study session start"""
    logger.info(f"STUDY_SESSION_STARTED - Deck ID: {deck_id}, Cards: {card_count}")

def log_study_session_completed(deck_id, cards_reviewed):
    """Log study session completion"""
    logger.info(f"STUDY_SESSION_COMPLETED - Deck ID: {deck_id}, Reviewed: {cards_reviewed}")

def log_card_rated(card_id, rating):
    """Log card rating"""
    logger.debug(f"CARD_RATED - Card ID: {card_id}, Rating: {rating}")

def log_api_call(provider, success, duration=None):
    """Log API call"""
    status = "SUCCESS" if success else "FAILED"
    msg = f"API_CALL - Provider: {provider}, Status: {status}"
    if duration:
        msg += f", Duration: {duration}s"
    logger.info(msg)

def log_tts_playback(card_id, success):
    """Log TTS playback"""
    status = "SUCCESS" if success else "FAILED"
    logger.debug(f"TTS_PLAYBACK - Card ID: {card_id}, Status: {status}")

def log_database_error(operation, error):
    """Log database error"""
    logger.error(f"DATABASE_ERROR - Operation: {operation}, Error: {str(error)}")

def log_user_action(action, details=""):
    """Log general user action"""
    logger.info(f"USER_ACTION - {action} {details}")

# Initialize logging
log_info("=" * 60)
log_info("AI Flashcards Application Started")
log_info("=" * 60)
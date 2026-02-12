from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import database as db
import ai_generator
from tts_player import TTSPlayer
from spaced_repetition import calculate_next_review, get_quality_from_rating
from hotkeys import HotkeyListener
import PyPDF2
import io
import os
from datetime import datetime
import logger
import analytics
import visualizations
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Global instances
tts_player = TTSPlayer()
hotkey_listener = HotkeyListener()

# Initialize database
db.init_db()

# Study session state
study_session = {
    'active': False,
    'deck_id': None,
    'cards': [],
    'current_index': 0,
    'current_card': None,
    'should_reload': False
}

@app.route('/')
def index():
    """Home page"""
    decks = db.get_all_decks()
    return render_template('index.html', decks=decks)

@app.route('/statistics')
def statistics():
   """Statistics and analytics page"""
   try:
       stats = analytics.get_study_statistics()
       deck_stats = analytics.get_deck_statistics()
       retention_metrics = analytics.calculate_retention_metrics()
       numerical_stats = analytics.get_numerical_statistics()
       correlations = analytics.calculate_correlation_matrix()
       
       charts = {
           'summary': visualizations.generate_overall_summary_chart(stats),
           'deck_progress': visualizations.generate_deck_progress_chart(deck_stats),
           'interval_dist': visualizations.generate_interval_distribution_chart(
               analytics.get_interval_distribution()
           ),
           'difficulty_dist': visualizations.generate_difficulty_distribution_chart(
               analytics.get_easiness_distribution()
           ),
           'upcoming': visualizations.generate_upcoming_reviews_chart(
               analytics.get_upcoming_reviews(7)
           ),
           'retention': visualizations.generate_retention_metrics_chart(retention_metrics)
       }
       
       logger.log_user_action("VIEW_STATISTICS")
       
       return render_template('statistics.html', 
                            stats=stats, 
                            charts=charts,
                            retention_metrics=retention_metrics,
                            numerical_stats=numerical_stats,
                            correlations=correlations)
   except Exception as e:
       logger.log_error("Error generating statistics", e)

@app.route('/create_deck', methods=['GET', 'POST'])
def create_deck():
    """Create a new deck"""
    if request.method == 'POST':
        deck_name = request.form.get('deck_name')
        
        if deck_name:
            deck_id = db.create_deck(deck_name)
            if deck_id:
                logger.log_deck_created(deck_name, deck_id)
                return redirect(url_for('view_deck', deck_id=deck_id))
            else:
                return render_template('create_deck.html', error="Deck name already exists")
        
        return render_template('create_deck.html', error="Deck name is required")
    
    return render_template('create_deck.html')

@app.route('/deck/<int:deck_id>')
def view_deck(deck_id):
    """View a deck and its cards"""
    deck = db.get_deck_by_id(deck_id)
    if not deck:
        return redirect(url_for('index'))
    
    cards = db.get_cards_by_deck(deck_id)
    due_cards = db.get_due_cards(deck_id)
    
    return render_template('view_deck.html', deck=deck, cards=cards, due_count=len(due_cards))

@app.route('/deck/<int:deck_id>/delete', methods=['POST'])
def delete_deck(deck_id):
    """Delete a deck"""
    db.delete_deck(deck_id)
    return redirect(url_for('index'))

@app.route('/deck/<int:deck_id>/generate', methods=['GET', 'POST'])
def generate_cards(deck_id):
    """Generate flashcards using AI"""
    deck = db.get_deck_by_id(deck_id)
    if not deck:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get form data
        num_cards = int(request.form.get('num_cards', 10))
        text_input = request.form.get('text_input', '').strip()
        pdf_file = request.files.get('pdf_file')
        
        # Extract text from PDF if provided
        if pdf_file and pdf_file.filename:
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
                pdf_text = ''
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text() + '\n'
                
                text_input = pdf_text if not text_input else text_input + '\n\n' + pdf_text
            except Exception as e:
                return jsonify({'error': f'Error reading PDF: {str(e)}'}), 400
        
        if not text_input:
            return jsonify({'error': 'Please provide study material (text or PDF)'}), 400
        
        # Get API settings
        settings = db.get_settings()
        if not settings['api_key']:
            return jsonify({'error': 'Please configure API key in settings'}), 400
        
        try:
            # Generate flashcards using AI
            flashcards = ai_generator.generate_flashcards(
                text_input,
                num_cards,
                settings['api_provider'],
                settings['api_key']
            )
            
            logger.log_cards_generated(deck_id, len(flashcards), settings['api_provider'])

            # Save flashcards to database
            db.add_cards_bulk(deck_id, flashcards)
            
            return jsonify({'success': True, 'count': len(flashcards)})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('view_deck.html', deck=deck)

@app.route('/card/<int:card_id>/edit', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit a card"""
    card = db.get_card_by_id(card_id)
    if not card:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        
        if question and answer:
            db.update_card(card_id, question, answer)
            return redirect(url_for('view_deck', deck_id=card['deck_id']))
    
    return render_template('edit_card.html', card=card)

@app.route('/card/<int:card_id>/delete', methods=['POST'])
def delete_card(card_id):
    """Delete a card"""
    card = db.get_card_by_id(card_id)
    if card:
        deck_id = card['deck_id']
        db.delete_card(card_id)
        return redirect(url_for('view_deck', deck_id=deck_id))
    
    return redirect(url_for('index'))

@app.route('/study/<int:deck_id>')
def study(deck_id):
    """Start a study session"""
    deck = db.get_deck_by_id(deck_id)
    if not deck:
        return redirect(url_for('index'))
    
    due_cards = db.get_due_cards(deck_id)
    
    if not due_cards:
        return render_template('study.html', deck=deck, no_cards=True)
    
    logger.log_study_session_started(deck_id, len(due_cards))

    # Initialize study session
    study_session['active'] = True
    study_session['deck_id'] = deck_id
    study_session['cards'] = [dict(card) for card in due_cards]
    study_session['current_index'] = 0
    study_session['current_card'] = study_session['cards'][0]
    
    # Get hotkey settings
    settings = db.get_settings()
    
    # Register hotkeys for study session
    try:
        hotkey_listener.register_hotkeys(
            settings['hotkey_again'],
            settings['hotkey_hard'],
            settings['hotkey_good'],
            settings['hotkey_easy'],
            lambda: rate_card_hotkey('again'),
            lambda: rate_card_hotkey('hard'),
            lambda: rate_card_hotkey('good'),
            lambda: rate_card_hotkey('easy')
        )
    except Exception as e:
        print(f"Warning: Could not register hotkeys: {e}")
    
    return render_template('study.html', 
                         deck=deck, 
                         card=study_session['current_card'],
                         current=1,
                         total=len(due_cards),
                         settings=settings)
    logger.log_study_session_started(deck_id, len(due_cards))

@app.route('/study/play_card', methods=['POST'])
def play_card():
    """Play current card with TTS"""
    if not study_session['active'] or not study_session['current_card']:
        return jsonify({'error': 'No active study session'}), 400
    
    card = study_session['current_card']
    
    def on_complete():
        pass  # Card playback complete, waiting for user rating
    
    tts_player.play_card(card['question'], card['answer'], pause_duration=10, on_complete=on_complete)
    
    return jsonify({'success': True})

@app.route('/study/speak_again', methods=['POST'])
def speak_again():
    """Speak the current card again"""
    if not study_session['active'] or not study_session['current_card']:
        return jsonify({'error': 'No active study session'}), 400
    
    card = study_session['current_card']
    tts_player.speak_again(card['question'], card['answer'])
    
    return jsonify({'success': True})

@app.route('/study/pause', methods=['POST'])
def pause_playback():
    """Pause TTS playback"""
    tts_player.pause()
    return jsonify({'success': True})

@app.route('/study/resume', methods=['POST'])
def resume_playback():
    """Resume TTS playback"""
    tts_player.resume()
    return jsonify({'success': True})

@app.route('/study/rate', methods=['POST'])
def rate_card():
    """Rate the current card and move to next"""
    if not study_session['active'] or not study_session['current_card']:
        return jsonify({'error': 'No active study session'}), 400
    
    rating = request.json.get('rating')  # 'again', 'hard', 'good', 'easy'
    
    if rating not in ['again', 'hard', 'good', 'easy']:
        return jsonify({'error': 'Invalid rating'}), 400
    
    return process_rating(rating)

def rate_card_hotkey(rating):
    """Handle rating from hotkey press"""
    if study_session['active'] and study_session['current_card']:
        print(f"\n🎹 HOTKEY PRESSED: {rating.upper()}")
        
        card = study_session['current_card']
        
        # Calculate next review using SM-2
        quality = get_quality_from_rating(rating)
        new_ef, new_interval, new_reps, next_review = calculate_next_review(
            quality,
            card['easiness_factor'],
            card['interval'],
            card['repetitions']
        )
        
        # Update card in database
        db.update_card_review(card['id'], new_ef, new_interval, new_reps, next_review)
        logger.log_card_rated(card['id'], rating)
        
        # Stop current TTS
        tts_player.stop()
        
        # Move to next card
        study_session['current_index'] += 1
        
        if study_session['current_index'] < len(study_session['cards']):
            # Load next card
            study_session['current_card'] = study_session['cards'][study_session['current_index']]
            study_session['should_reload'] = True
            print(f"✅ Next card loaded. Page will reload.")
        else:
            # Session complete
            study_session['should_reload'] = True
            study_session['current_card'] = None
            print("✅ Session complete.")

def process_rating(rating):
    """Process card rating and update database"""
    card = study_session['current_card']
    
    # Calculate next review using SM-2
    quality = get_quality_from_rating(rating)
    new_ef, new_interval, new_reps, next_review = calculate_next_review(
        quality,
        card['easiness_factor'],
        card['interval'],
        card['repetitions']
    )
    
    # Update card in database
    db.update_card_review(card['id'], new_ef, new_interval, new_reps, next_review)

    logger.log_card_rated(card['id'], rating)
    
    # Stop current TTS
    tts_player.stop()
    
    # Move to next card
    study_session['current_index'] += 1
    
    if study_session['current_index'] < len(study_session['cards']):
        # Load next card
        study_session['current_card'] = study_session['cards'][study_session['current_index']]
        
        # Auto-play next card
        card = study_session['current_card']
        tts_player.play_card(card['question'], card['answer'], pause_duration=10)
        
        return jsonify({
            'success': True,
            'next_card': True,
            'card': study_session['current_card'],
            'current': study_session['current_index'] + 1,
            'total': len(study_session['cards'])
        })
    else:
        # Session complete
        end_study_session()
        return jsonify({'success': True, 'session_complete': True})
    logger.log_card_rated(card['id'], rating)

@app.route('/study/end', methods=['POST'])
def end_study():
    """End the study session"""
    end_study_session()
    return jsonify({'success': True})

def end_study_session():
    """Clean up study session"""
    if study_session['deck_id'] and study_session['current_index'] > 0:
        logger.log_study_session_completed(
            study_session['deck_id'], 
            study_session['current_index']
        )
    tts_player.stop()
    hotkey_listener.unregister_hotkeys()
    
    study_session['active'] = False
    study_session['deck_id'] = None
    study_session['cards'] = []
    study_session['current_index'] = 0
    study_session['current_card'] = None
    logger.log_study_session_completed(study_session['deck_id'], study_session['current_index'])

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page"""
    if request.method == 'POST':
        api_provider = request.form.get('api_provider')
        api_key = request.form.get('api_key')
        hotkey_again = request.form.get('hotkey_again')
        hotkey_hard = request.form.get('hotkey_hard')
        hotkey_good = request.form.get('hotkey_good')
        hotkey_easy = request.form.get('hotkey_easy')
        
        db.update_settings(api_provider, api_key, hotkey_again, hotkey_hard, hotkey_good, hotkey_easy)
        
        return redirect(url_for('settings'))
    
    current_settings = db.get_settings()
    return render_template('settings.html', settings=current_settings)

@app.route('/algorithm')
def algorithm():
    """SM-2 Algorithm explanation page"""
    return render_template('algorithm.html')

@app.route('/study/check_update', methods=['POST'])
def check_update():
    """Check if page should reload due to hotkey"""
    if study_session['should_reload']:
        study_session['should_reload'] = False
        return jsonify({'reload': True})
    
    return jsonify({'reload': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
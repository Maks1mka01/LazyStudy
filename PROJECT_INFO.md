# Project Documentation: AI Flashcards Application

## Project Overview

**Title**: AI-Powered Spaced Repetition Flashcard Application  
**Language**: Python 3.8+  
**Framework**: Flask (Web Framework)  
**Database**: SQLite3  
**Purpose**: Educational tool for creating and studying flashcards using AI and spaced repetition

## Motivation

This application addresses the needs of:
- **ADHD learners** who benefit from audio-based, hands-free studying
- **Multitaskers** who want to study while doing other activities
- **Busy students** who need efficient, scientifically-backed study methods

## Core Technologies

### Required Libraries
```
Flask==3.0.0          # Web framework
requests==2.31.0      # HTTP library for API calls
pyttsx3==2.90        # Text-to-speech engine (offline)
keyboard==0.13.5      # Global hotkey support
PyPDF2==3.0.1        # PDF text extraction
```

### Python Built-ins Used
- `sqlite3` - Database operations
- `datetime` - Date/time handling for spaced repetition
- `json` - JSON parsing for AI responses
- `threading` - Asynchronous TTS playback
- `io` - File handling

## Architecture

### Project Structure
```
anki_ai_app/
├── app.py                    # Main Flask application & routing
├── database.py               # SQLite database operations
├── ai_generator.py           # AI API integration
├── tts_player.py            # Text-to-speech player
├── spaced_repetition.py     # SM-2 algorithm implementation
├── hotkeys.py               # Global hotkey listener
├── templates/               # HTML templates (Jinja2)
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── create_deck.html    # Deck creation form
│   ├── view_deck.html      # Deck management & card generation
│   ├── edit_card.html      # Card editing form
│   ├── study.html          # Study session interface
│   └── settings.html       # API & hotkey configuration
├── static/
│   └── style.css           # CSS styling
├── flashcards.db           # SQLite database (auto-created)
└── requirements.txt         # Python dependencies
```

### Database Schema

#### Decks Table
```sql
CREATE TABLE decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Cards Table
```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    easiness_factor REAL DEFAULT 2.5,    -- SM-2 algorithm
    interval INTEGER DEFAULT 0,           -- Days until next review
    repetitions INTEGER DEFAULT 0,        -- Successful review count
    next_review TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE
);
```

#### Settings Table
```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    api_provider TEXT DEFAULT 'groq',
    api_key TEXT,
    hotkey_again TEXT DEFAULT 'ctrl+1',
    hotkey_hard TEXT DEFAULT 'ctrl+2',
    hotkey_good TEXT DEFAULT 'ctrl+3',
    hotkey_easy TEXT DEFAULT 'ctrl+4'
);
```

## Core Components

### 1. Flask Application (app.py)

**Routes**:
- `/` - Home page (deck list)
- `/create_deck` - Create new deck
- `/deck/<id>` - View deck and manage cards
- `/deck/<id>/generate` - AI card generation
- `/deck/<id>/delete` - Delete deck
- `/card/<id>/edit` - Edit card
- `/card/<id>/delete` - Delete card
- `/study/<id>` - Study session
- `/study/*` - Study controls (play, pause, rate, etc.)
- `/settings` - API and hotkey configuration

**Key Features**:
- Session management for study state
- Global TTS player instance
- Global hotkey listener instance
- RESTful API endpoints for AJAX calls

### 2. Database Module (database.py)

**Functions**:
- `init_db()` - Initialize database tables
- Deck CRUD operations
- Card CRUD operations
- Settings management
- Query helpers for due cards

**Design Pattern**: Connection pooling with context managers

### 3. AI Generator (ai_generator.py)

**Supported Providers**:
1. **Groq** - llama-3.1-8b-instant model
2. **OpenRouter** - meta-llama/llama-3.1-8b-instruct:free
3. **Together AI** - Meta-Llama-3.1-8B-Instruct-Turbo

**Process**:
1. Constructs prompt with study material
2. Requests JSON-formatted flashcards
3. Parses AI response
4. Validates card format
5. Returns list of question/answer pairs

**Error Handling**:
- API connection errors
- JSON parsing errors
- Invalid response format
- Rate limiting

### 4. Spaced Repetition (spaced_repetition.py)

**SM-2 Algorithm Implementation**:
- Quality ratings: 0 (Again), 1 (Hard), 2 (Good), 3 (Easy)
- Easiness Factor (EF): Adjusted based on performance
- Interval calculation: Days until next review
- Repetition counter: Tracks successful reviews

**Algorithm Logic**:
```python
if quality < 2:  # Again/Hard
    repetitions = 0
    interval = 1 day
else:  # Good/Easy
    repetitions += 1
    if repetitions == 1:
        interval = 1 day
    elif repetitions == 2:
        interval = 6 days
    else:
        interval = previous_interval * easiness_factor
    
    if quality == 3:  # Easy bonus
        interval *= 1.3
```

### 5. Text-to-Speech Player (tts_player.py)

**Features**:
- Asynchronous playback using threading
- 10-second pause between question and answer
- Pause/resume functionality
- Stop/cancel functionality
- "Speak Again" for immediate replay

**Design Pattern**: 
- Observer pattern for completion callbacks
- Thread-safe state management
- Flag-based control flow

### 6. Hotkey Listener (hotkeys.py)

**Features**:
- Global hotkey registration
- Callback-based event handling
- Clean unregistration on session end
- Suppression of default key behavior

**Platform Considerations**:
- Windows: Requires administrator privileges
- macOS: Requires accessibility permissions
- Linux: May require X11 or Wayland permissions

## Key Algorithms

### 1. SuperMemo SM-2 Algorithm
The application uses the original SM-2 algorithm for optimal spaced repetition:

**Variables**:
- EF (Easiness Factor): 1.3 to 2.5+
- I (Interval): Days until next review
- n (Repetitions): Count of successful reviews

**Benefits**:
- Proven effectiveness (used by Anki)
- Simple implementation
- Adjusts to individual card difficulty

### 2. AI Prompt Engineering
The application constructs prompts that:
- Request specific JSON format
- Include examples for clarity
- Specify exact number of cards
- Guide AI to create Q&A pairs suitable for flashcards

## Implementation Highlights

### 1. Minimal Design Philosophy
- Only necessary libraries included
- No heavy frameworks (NumPy, Pandas, Matplotlib not needed)
- SQLite instead of external database
- Offline TTS instead of API-based TTS

### 2. Flask Integration
- Template inheritance for DRY code
- AJAX for dynamic card generation
- Session state for study flow
- Static file serving for CSS

### 3. User Experience
- Auto-advance between cards
- Visual progress indicator
- Hotkey hints on buttons
- Responsive error messages
- Loading states during AI generation

### 4. PDF Processing
Uses PyPDF2 to:
- Read PDF files
- Extract text from all pages
- Combine with user-provided text
- Handle multi-page documents

## Challenges & Solutions

### Challenge 1: TTS Blocking UI
**Problem**: pyttsx3 blocks the main thread  
**Solution**: Threading for async playback

### Challenge 2: Global Hotkeys
**Problem**: Requires elevated privileges  
**Solution**: Graceful fallback to button clicks, clear user instructions

### Challenge 3: AI Response Parsing
**Problem**: AI sometimes adds markdown or extra text  
**Solution**: Robust parsing with strip/find logic for JSON extraction

### Challenge 4: Study Session State
**Problem**: HTTP is stateless  
**Solution**: In-memory session dict for active study state

## Testing Recommendations

### Manual Testing Checklist
- [ ] Create deck
- [ ] Generate cards (PDF and text input)
- [ ] Edit cards
- [ ] Delete cards
- [ ] Study session flow
- [ ] Hotkey functionality
- [ ] TTS playback (play, pause, speak again)
- [ ] Rating cards (all 4 options)
- [ ] Spaced repetition scheduling
- [ ] Settings persistence
- [ ] Multiple deck management

### Error Scenarios to Test
- [ ] Invalid API key
- [ ] Network disconnection during generation
- [ ] Empty study material
- [ ] Corrupted PDF
- [ ] Hotkey conflicts
- [ ] Multiple study sessions

## Performance Considerations

### Database
- Indexed foreign keys for fast queries
- Compound queries reduce roundtrips
- Single connection per request

### AI Generation
- Timeout set to 60 seconds
- User sees loading indicator
- Async processing possibility for future

### TTS
- Threaded to avoid blocking
- Stop mechanism prevents overlap
- Lightweight engine (pyttsx3)

## Security Considerations

### API Keys
- Stored in local database only
- Not transmitted except to AI provider
- Masked in UI (password field)

### User Data
- All data stored locally
- No external tracking
- No cloud synchronization

### Input Validation
- SQL injection prevention (parameterized queries)
- XSS prevention (Flask template escaping)
- File type validation (PDF only)

## Future Enhancements

### Technical Improvements
1. Add unit tests (pytest)
2. Implement caching for repeated AI queries
3. Add export/import (JSON format)
4. Browser-based TTS as alternative
5. Progressive Web App (PWA) support

### Feature Additions
1. Image occlusion flashcards
2. Statistics dashboard
3. Deck sharing via JSON
4. Custom card templates
5. Mobile app version

### Algorithm Enhancements
1. FSRS algorithm (newer than SM-2)
2. Machine learning for personalized intervals
3. Adaptive pause duration
4. Confidence ratings

## Conclusion

This project demonstrates:
- Full-stack Python development
- Flask web framework usage
- SQLite database design
- External API integration
- Algorithm implementation (SM-2)
- Asynchronous programming
- User interface design
- File processing (PDF)
- System integration (hotkeys, TTS)

The application successfully combines multiple technologies to create a useful educational tool while maintaining minimal dependencies and local-first design.

## References

- SuperMemo SM-2 Algorithm: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
- Flask Documentation: https://flask.palletsprojects.com/
- pyttsx3 Documentation: https://pyttsx3.readthedocs.io/
- Anki Algorithm: https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html
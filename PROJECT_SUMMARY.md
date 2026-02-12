# Project Summary: AI Flashcards Application

## Project Overview

An AI-powered flashcard application that helps students study efficiently using:
- **AI-generated flashcards** from study materials (PDFs or text)
- **Text-to-speech** for hands-free studying  
- **Spaced repetition** algorithm (SM-2) for optimal retention
- **Global hotkeys** for fast card ratings
- **Local storage** with SQLite database

Perfect for ADHD learners, multitaskers, and anyone who wants an efficient study tool!

---

## Technical Specifications

### Core Technologies
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Python 3.8+** | Programming language | Required for project |
| **Flask** | Web framework | Lightweight, easy to use |
| **SQLite3** | Database | Built-in, no setup needed |
| **pyttsx3** | Text-to-speech | Offline, no API costs |
| **keyboard** | Hotkey support | Global shortcuts |
| **PyPDF2** | PDF parsing | Extract text from PDFs |
| **requests** | HTTP library | AI API calls |

### Why These Libraries?
- **Minimal** - Only 5 external packages
- **Essential** - Each serves a specific need
- **No bloat** - No NumPy, Pandas, or Matplotlib (not needed)

---

## Architecture

### File Structure (9 files + templates + static)
```
anki_ai_app/
├── app.py                    # Flask routes & application logic
├── database.py               # SQLite operations (CRUD)
├── ai_generator.py           # AI API integration (3 providers)
├── tts_player.py            # Text-to-speech with threading
├── spaced_repetition.py     # SM-2 algorithm
├── hotkeys.py               # Global hotkey listener
├── templates/ (7 files)     # HTML templates
├── static/style.css         # CSS styling
└── requirements.txt         # Dependencies
```

### Database Design (3 tables)
1. **decks** - Store flashcard decks
2. **cards** - Store questions, answers, and SM-2 data
3. **settings** - API keys and hotkey configuration

---

## Key Features Implemented

### 1. AI Card Generation
- **3 AI providers**: Groq, OpenRouter, Together AI (all free)
- **PDF support**: Upload PDFs to extract text
- **Custom count**: User chooses how many cards to generate
- **Error handling**: Graceful failures with user feedback

### 2. Spaced Repetition (SM-2 Algorithm)
- **4 rating levels**: Again, Hard, Good, Easy
- **Smart scheduling**: Cards appear at optimal intervals
- **Data persistence**: Review schedule saved in database
- **Proven effectiveness**: Same algorithm as Anki

### 3. Text-to-Speech Study Mode
- **Auto-play**: Reads question → 10s pause → reads answer
- **Controls**: Play, Pause, Speak Again
- **Threading**: Non-blocking audio playback
- **Auto-advance**: Next card plays after rating

### 4. Global Hotkeys
- **Customizable**: Set any key combinations
- **Fast workflow**: Rate cards without clicking
- **Platform support**: Windows, macOS, Linux

### 5. Deck Management
- **Multiple decks**: Organize by topic
- **Edit cards**: Fix AI-generated cards
- **Delete cards**: Remove unwanted cards
- **Statistics**: See due count and total cards

---

## Algorithm Implementation

### SuperMemo SM-2 Spaced Repetition
```python
# Quality ratings map to intervals:
Again (0)  → Reset to 1 day
Hard (1)   → Reset to 1 day  
Good (2)   → 1 day → 6 days → ~15 days → ~38 days...
Easy (3)   → 30% longer intervals than Good

# Easiness Factor adjusts based on performance:
EF = EF + (0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02))
Minimum EF = 1.3
```

**Why SM-2?**
- Scientifically proven for retention
- Used by Anki (gold standard)
- Simple to implement
- Adaptive to card difficulty

---

## User Interface

### Pages
1. **Home** - Deck list with due counts
2. **Create Deck** - Simple form for new decks
3. **View Deck** - Card generation and management
4. **Edit Card** - Modify question/answer
5. **Study** - TTS playback and rating interface
6. **Settings** - API and hotkey configuration

### Design Philosophy
- **Clean & minimal** - No clutter
- **Responsive** - Works on different screen sizes
- **Intuitive** - Clear labels and actions
- **Accessible** - Keyboard shortcuts for power users

---

## User Workflow

```
1. Configure API key in Settings
   ↓
2. Create a Deck
   ↓
3. Upload PDF or paste text → Generate cards
   ↓
4. Review/edit generated cards (optional)
   ↓
5. Click "Study Now"
   ↓
6. Listen → Think → Rate → Auto-advance
   ↓
7. Cards scheduled by SM-2 algorithm
   ↓
8. Return daily to review due cards
```

---

## Innovation & Problem-Solving

### Problem 1: Hands-Free Studying
**Solution**: TTS audio + auto-advance + hotkeys  
**Impact**: Study while multitasking (cooking, exercising, etc.)

### Problem 2: Manual Card Creation
**Solution**: AI generates flashcards from any text  
**Impact**: Save hours of card creation time

### Problem 3: Forgetting Curve
**Solution**: SM-2 spaced repetition algorithm  
**Impact**: Optimal retention with minimal effort

### Problem 4: Platform Accessibility
**Solution**: Flask web app (runs anywhere)  
**Impact**: Cross-platform, no app store needed

---

## Technical Achievements

### Backend
- RESTful API design
- Database normalization (3 tables, foreign keys)
- Parameterized queries (SQL injection prevention)
- Error handling and user feedback
- Session state management

### Frontend
- Template inheritance (DRY principle)
- AJAX for async operations
- Responsive CSS grid layout
- Form validation
- Loading states and spinners

### Integration
- Multiple AI API integration
- PDF text extraction
- Threading for TTS
- Global hotkey registration
- JSON parsing and validation

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

1. **Python Programming**
   - Object-oriented design
   - Threading and concurrency
   - Error handling
   - External library integration

2. **Web Development**
   - Flask framework
   - HTML/CSS
   - JavaScript (AJAX)
   - RESTful APIs

3. **Database Management**
   - SQLite schema design
   - CRUD operations
   - Data relationships
   - Query optimization

4. **Software Engineering**
   - Modular code structure
   - Documentation
   - Version control ready (.gitignore)
   - User-centric design

5. **Algorithm Implementation**
   - SM-2 spaced repetition
   - State management
   - Callback patterns
   - Asynchronous operations

---

## Project Statistics

- **Lines of Code**: ~2,000+
- **Python Files**: 6 core modules
- **Templates**: 7 HTML files
- **External APIs**: 3 integrations
- **Database Tables**: 3
- **Features**: 15+
- **Dependencies**: 5 (minimal!)

---

## Future Enhancements

### Possible Extensions
1. **Statistics Dashboard** - Track study progress
2. **Import/Export** - Share decks via JSON
3. **Image Support** - Add images to flashcards
4. **Mobile App** - React Native version
5. **Cloud Sync** - Optional cloud backup
6. **Custom Algorithms** - FSRS (newer than SM-2)
7. **Gamification** - Streaks and achievements
8. **Collaborative Decks** - Share with classmates

---

## Project Goals

### Requirements Met
- **Python-based** - Core language requirement
- **Flask framework** - Web framework as requested
- **SQLite database** - Local storage requirement
- **Minimal libraries** - Only essential packages
- **AI integration** - Multiple free API options
- **PDF parsing** - Extract text from documents
- **TTS playback** - Hands-free studying
- **Spaced repetition** - SM-2 algorithm
- **Hotkey support** - Global keyboard shortcuts
- **Card management** - Create, edit, delete
- **Multi-deck support** - Organize by topic

### Bonus Features
- **3 AI providers** - Flexibility and redundancy
- **Auto-advance** - Seamless study flow
- **Pause/Resume** - Study control
- **Settings persistence** - Save preferences
- **Responsive design** - Mobile-friendly
- **Clean UI** - Professional appearance
- **Error handling** - User-friendly messages

---

## Presentation Points

### For Demo
1. Show deck creation (30 seconds)
2. Generate cards from sample text (1 minute)
3. Edit a generated card (30 seconds)
4. Study session with TTS and hotkeys (2 minutes)
5. Show settings and API configuration (30 seconds)

### Key Talking Points
- "Minimal dependencies - only what's needed"
- "Local-first - all data stored on device"
- "AI-powered - saves hours of manual work"
- "Science-backed - uses proven SM-2 algorithm"
- "Accessible - perfect for ADHD and multitaskers"

---

## Conclusion

This project successfully creates a **production-ready educational tool** that:
- Solves real problems for students
- Uses modern technologies effectively
- Maintains minimal dependencies
- Demonstrates full-stack development skills
- Implements proven algorithms
- Provides excellent user experience

**Impact**: Helps students study more efficiently while multitasking or dealing with attention challenges.

---

## Documentation Files

1. **README.md** - Installation and usage guide
2. **USAGE.md** - Quick start with examples  
3. **PROJECT_INFO.md** - Technical deep dive
4. **PROJECT_SUMMARY.md** - This file (high-level overview)

---

**Ready to submit? Good luck with your project!**
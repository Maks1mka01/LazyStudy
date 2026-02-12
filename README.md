# AI Flashcards - Spaced Repetition Learning App

A Python Flask application that generates AI-powered flashcards from study materials and uses spaced repetition (SM-2 algorithm) with text-to-speech for hands-free studying. Perfect for ADHD learners and multitaskers!

## Features

- **AI-Powered Card Generation**: Generate flashcards from PDFs or text using free AI APIs (OpenRouter, Groq, Together AI)
- **Text-to-Speech**: Hands-free studying with automatic TTS playback
- **Spaced Repetition**: SM-2 algorithm (like Anki) for optimal learning
- **Global Hotkeys**: Rate cards using keyboard shortcuts
- **Multiple Decks**: Organize flashcards by topic
- **Editable Cards**: Edit generated cards before studying
- **Local Storage**: All data stored on your device with SQLite

## Prerequisites

- Python 3.8 or higher
- An API key from one of these providers (all have free tiers):
  - [Groq](https://console.groq.com) - Fast and free
  - [OpenRouter](https://openrouter.ai) - Multiple models
  - [Together AI](https://api.together.xyz) - Open source models

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
cd anki_ai_app
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Open your browser** and go to:
```
http://localhost:5000
```

## Setup Guide

### 1. Configure API Settings

1. Click **Settings** in the navigation menu
2. Choose your AI provider (Groq recommended for beginners)
3. Enter your API key
4. Configure hotkeys (default: Ctrl+1/2/3/4)
5. Click **Save Settings**

### 2. Create Your First Deck

1. Click **New Deck** or **Create Deck**
2. Enter a deck name (e.g., "Biology Chapter 5")
3. Click **Create Deck**

### 3. Generate Flashcards

1. Open your deck
2. Choose number of cards to generate
3. Either:
   - Upload a PDF file, OR
   - Paste study material text
4. Click **Generate Flashcards**
5. Wait for AI to create cards (usually 10-30 seconds)

### 4. Edit Cards (Optional)

- Review generated cards
- Click **Edit** to modify question/answer
- Click **Delete** to remove unwanted cards

### 5. Study Session

1. Click **Study Now** on a deck with due cards
2. The app will automatically:
   - Read the question
   - Pause for 10 seconds (think time)
   - Read the answer
3. Rate your answer:
   - **Again** (Ctrl+1): Forgot completely - card resets
   - **Hard** (Ctrl+2): Difficult to remember
   - **Good** (Ctrl+3): Remembered correctly
   - **Easy** (Ctrl+4): Very easy - longer interval
4. Next card plays automatically!

### Study Controls

- **Play Card**: Start/restart current card audio
- **Pause**: Pause during thinking time
- **Speak Again**: Repeat current card immediately
- **End Session**: Stop studying and return to deck

## How It Works

### Spaced Repetition (SM-2 Algorithm)

The app uses the same algorithm as Anki:

- **New cards**: Reviewed after 1 day
- **Good rating**: Intervals increase (1 day → 6 days → ~2 weeks → ~1 month, etc.)
- **Easy rating**: 30% longer intervals
- **Hard/Again**: Shorter intervals or restart

### Hotkeys

**Note**: On Windows/Linux, you may need to run as administrator for global hotkeys to work.

Default hotkeys:
- `Ctrl+1` - Again
- `Ctrl+2` - Hard
- `Ctrl+3` - Good
- `Ctrl+4` - Easy

You can customize these in Settings.

## Tips for Best Results

### AI Card Generation

1. **Provide clear, structured text**: Textbook excerpts work better than random notes
2. **Optimal length**: 500-2000 words per generation
3. **Specify card count**: 10-20 cards for a page, 30-50 for a chapter
4. **Review before studying**: AI sometimes creates imperfect cards - edit them!

### Studying

1. **Study regularly**: Do reviews daily for best retention
2. **Use hotkeys**: Much faster than clicking buttons
3. **Be honest**: Rating cards accurately improves the algorithm
4. **Multitask-friendly**: Study while doing chores, exercising, etc.

## Troubleshooting

### "API Error" when generating cards

- Check your API key is correct
- Ensure you have credits/quota remaining
- Try a different provider

### Hotkeys not working

- **Windows/Linux**: Run as administrator
- **macOS**: Grant accessibility permissions
- Try simpler hotkeys (e.g., `F1`, `F2`, `F3`, `F4`)

### TTS not speaking

- Check your system audio is working
- Try adjusting volume in system settings
- Some systems may need additional TTS engines installed

### No cards due to study

- This means you've reviewed all cards!
- Wait until cards become due again
- Or generate more cards for the deck

## File Structure

```
anki_ai_app/
├── app.py                  # Flask application
├── database.py             # SQLite operations
├── ai_generator.py         # AI API calls
├── tts_player.py          # Text-to-speech
├── spaced_repetition.py   # SM-2 algorithm
├── hotkeys.py             # Global hotkey listener
├── templates/             # HTML templates
├── static/                # CSS styles
├── flashcards.db          # SQLite database (created on first run)
└── requirements.txt       # Python dependencies
```

## API Provider Comparison

| Provider | Speed | Free Tier | Best For |
|----------|-------|-----------|----------|
| **Groq** | Very Fast | Generous | Quick generation, recommended for beginners |
| **OpenRouter** | Medium | Multiple free models | Flexibility, trying different models |
| **Together AI** | Medium | Good limits | Open source models |

## Privacy & Security

- All data stored **locally** on your device
- API keys stored in local SQLite database
- Study material never stored by AI providers (only sent for processing)
- No telemetry or tracking

## Known Limitations

- Hotkeys require administrator/elevated privileges on some systems
- TTS voice quality depends on your system's TTS engine
- AI-generated cards may need editing for accuracy
- Large PDFs (>50 pages) may hit API token limits

## Future Improvements (Optional)

Ideas for extending the project:
- [ ] Import/export decks (JSON format)
- [ ] Statistics dashboard
- [ ] Image support in flashcards
- [ ] Custom TTS voices
- [ ] Mobile responsive design
- [ ] Batch card editing

## License

Free to use for educational purposes. Modify as needed for your Python project!

## Credits

- Built with Flask, SQLite, and Python
- Uses pyttsx3 for TTS
- Implements SuperMemo SM-2 algorithm
- AI providers: Groq, OpenRouter, Together AI

---

**Happy Learning!**
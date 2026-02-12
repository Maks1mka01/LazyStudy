# LazyStudy

An application that generates anki flashcards using AI from study materials and uses spaced repetition technique with text-to-speech for studying without any effort. It's perfect for people who don't want to try to study, but also want to prepare for exams or assignment's defense

## Features

- **AI Card Generation**: Generate flashcards from PDFs or text using free AI APIs (OpenRouter, Groq, Together AI)
- **TTS**: Effortless studying with automatic TTS playback
- **Spaced Repetition**: SM-2 algorithm for optimal learning
- **Global Hotkeys**: Rate cards using keyboard shortcuts
- **Statistics**: Statistics of your study progress displayed through graphics
- **Multiple Decks**: Organize flashcards by topic
- **Editable Cards**: Edit generated cards before studying
- **Local Storage**: All data stored on your device with SQLite

## Requirements

- Python 3.8 or higher
- An API key from one of these providers:
  - [Groq](https://console.groq.com)
  - [OpenRouter](https://openrouter.ai) 
  - [Together AI](https://api.together.xyz) 

## Installation

1. **Clone or download this repository**:
```bash
git clone
```

2. **Install dependencies**:
```bash
cd
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Open this link in browser**:
```
http://localhost:5000
```

## Setup Guide

### 1. Get API Key

1. Navigate to the one AI provider website
2. Sign up
3. Find and navigate to API Keys
4. Click "**New API Key**" button
5. Name it and click continue
6. Copy your prepared API key

### 2. Configure Settings

1. Navigate to settings menu
2. Copy and paste API key for your provider
3. Configure hotkeys (Default: ctrl+1, ctrl+2, ctrl+3, ctrl+4)
4. Click **Save Settings**

### 3. Create Your First Deck

1. Click **Create Deck** or **Create New Deck**
2. Enter a deck name
3. Click **Create Deck**

### 4. Generate Flashcards

1. Open your deck
2. Choose number of cards to generate
3. Paste either PDF file or text of study material:
4. Click **Generate Flashcards**
5. In case of error click **Generate Flashcards** again

### 5. Edit Cards

- This section contains all generated cards
- Click **Edit** to modify question or answer
- Click **Delete** to remove unnecessary cards

### 6. Study Session

1. Click **Study** on a deck with generated cards
2. Then the app will:
   - Read the question
   - Pause for 10 seconds
   - Read the answer
3. Rate your answer:
   - **Again** (Ctrl+1): If you don't know the answer
   - **Hard** (Ctrl+2): Understood the question but still can't answer
   - **Good** (Ctrl+3): Remembered correctly
   - **Easy** (Ctrl+4): If you easily answered the question
4. Next card plays

### 7. Statistics

1. Click **Statistics** button on top right corner
2. Review your study progress

### Study Controls

- **Pause**: Pause during thinking time
- **Resume**: Resume to continue studying 
- **Speak Again**: Repeat audio for a current card
- **End Session**: Stop studying and return to deck

## How It Works

### Spaced Repetition (SM-2 Algorithm)

This algorithm is the same one used in Anki:

- **New cards**: Reviewed after 1 day
- **Good rating**: Intervals increase (1 day → 6 days → ~2 weeks → ~1 month, etc.)
- **Easy rating**: 30% longer intervals
- **Hard/Again**: Shorter intervals or restart

For more information about algorithm used, check separate page "SM-2 Algorithm" in our app.

## API Provider Comparison

- Groq (**Recommended for beginnders**)
- OpenRouter (**Has different models**)
- Together AI (**Option if nothing works**)
## License

Free to use for educational purposes. Modify as needed for your Python project!

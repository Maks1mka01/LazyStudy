import requests
import json

def generate_flashcards(text, num_cards, api_provider, api_key):
    """
    Generate flashcards from text using AI API
    
    Args:
        text: Study material text
        num_cards: Number of flashcards to generate
        api_provider: 'openrouter', 'groq', or 'together'
        api_key: API key for the provider
    
    Returns:
        list: List of dicts with 'question' and 'answer' keys
    """
    
    prompt = f"""Generate exactly {num_cards} flashcards from the following study material. 
Each flashcard should have a clear question and a concise answer.
Format your response as a JSON array of objects with 'question' and 'answer' fields.

Example format:
[
    {{"question": "What is photosynthesis?", "answer": "The process by which plants convert light energy into chemical energy"}},
    {{"question": "What are the main products of photosynthesis?", "answer": "Glucose and oxygen"}}
]

Study Material:
{text}

Generate exactly {num_cards} flashcards in the JSON format shown above. Return ONLY the JSON array, no additional text."""

    try:
        if api_provider == 'openrouter':
            return _call_openrouter(prompt, api_key)
        elif api_provider == 'groq':
            return _call_groq(prompt, api_key)
        elif api_provider == 'together':
            return _call_together(prompt, api_key)
        else:
            raise ValueError(f"Unknown API provider: {api_provider}")
    except Exception as e:
        raise Exception(f"Error generating flashcards: {str(e)}")

def _call_openrouter(prompt, api_key):
    """Call OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",  # Free model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    return _parse_flashcards(content)

def _call_groq(prompt, api_key):
    """Call Groq API"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",  # Fast and free
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    return _parse_flashcards(content)

def _call_together(prompt, api_key):
    """Call Together AI API"""
    url = "https://api.together.xyz/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    return _parse_flashcards(content)

def _parse_flashcards(content):
    """Parse AI response to extract flashcards"""
    # Try to find JSON in the response
    content = content.strip()
    
    # Remove markdown code blocks if present
    if content.startswith('```'):
        lines = content.split('\n')
        content = '\n'.join(lines[1:-1])
    
    # Remove any text before the first [ or after the last ]
    start_idx = content.find('[')
    end_idx = content.rfind(']')
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError("Could not find JSON array in response")
    
    json_str = content[start_idx:end_idx+1]
    
    try:
        flashcards = json.loads(json_str)
        
        # Validate format
        if not isinstance(flashcards, list):
            raise ValueError("Response is not a list")
        
        for card in flashcards:
            if 'question' not in card or 'answer' not in card:
                raise ValueError("Invalid flashcard format")
        
        return flashcards
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}")
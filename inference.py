import os
import requests
import random

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-20b")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co")

def generate_question(difficulty: str, asked_questions: list):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    
    # We construct the URL depending on the router pattern.
    api_url = f"{API_BASE_URL}/models/{MODEL_NAME}"
    
    topic = random.choice(["Python", "Machine Learning", "System Design", "SQL", "Data Structures", "Algorithms", "APIs"])
    str_asked = ", ".join(asked_questions) if asked_questions else "None"
    
    prompt = f"[INST] You are a highly professional technical interviewer. Generate strictly ONE {difficulty} interview question about {topic}. Provide only the question, no greetings, no introductory text, no explanations. Avoid asking these questions: {str_asked}. [/INST]"
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7, "return_full_text": False}
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                return result[0]['generated_text'].strip()
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text'].strip()
        else:
            print(f"HF API returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error calling Hugging Face API: {e}")
        
    # Graceful fallback questions to ensure system keeps working
    fallbacks = [
        "How would you optimize a significantly slow-running SQL query?",
        "Explain the primary difference between deep learning and traditional machine learning pipelines.",
        "What are the main benefits of using a generator in Python for large datasets?",
        "Describe a time when you had to design a highly concurrent, scalable web system.",
        "How do you handle memory leaks in a long-running backend application?",
        "Explain the CAP theorem and provide an example of when you would choose Availability over Consistency."
    ]
    return random.choice(fallbacks)

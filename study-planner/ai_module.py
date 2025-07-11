import requests

def generate_reviewer(subject, topic, notes):
    prompt = (
        f"You are an expert study assistant. "
        f"Create a comprehensive reviewer for the following:\n"
        f"Subject: {subject}\n"
        f"Topic: {topic}\n"
        f"Notes: {notes}\n\n"
        f"First, summarize the notes. Then, expand on the topic by including related concepts, important facts, and tips for understanding. "
        f"Make it clear, concise, and helpful for exam review."
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    data = response.json()
    return data.get("response", "No response from Ollama.")
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)

# Load a local free AI model (like DistilGPT2) for generating answers
generator = pipeline('text-generation', model='distilgpt2')

def search_google(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        return results[0].get_text() if results else "No results found online."
    except:
        return "Could not search online."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"answer": "Please ask a valid question."})

    # Step 1: Try to get an answer from Google search
    google_answer = search_google(question)

    # Step 2: Generate a smart AI answer using local model
    ai_answer = generator(question, max_length=100, num_return_sequences=1)[0]['generated_text']

    # Combine both answers
    final_answer = f"Online Info: {google_answer}\nAI Suggestion: {ai_answer}"
    
    return jsonify({"answer": final_answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

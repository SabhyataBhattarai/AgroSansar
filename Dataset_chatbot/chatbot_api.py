from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Optional: Translator for Nepali
try:
    from translate import Translator
except ImportError:
    Translator = None

# -------------------
# Load questions, answers, and embeddings
# -------------------
with open("question_embeddings.pkl", "rb") as f:
    questions, answers, embeddings = pickle.load(f)

# Load multilingual model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# -------------------
# Route: Ask question
# -------------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("question", "").strip()
    language = data.get("language", "en")  # default English

    if not user_input:
        return jsonify({"answer": "Please ask a question." if language == "en" else "कृपया प्रश्न राख्नुहोस्।"})

    # Encode input and find best match
    threshold = 0.55  # Adjust for sensitivity
    query_embedding = model.encode([user_input])
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    if best_score < threshold:
        bot_reply = "Sorry, I don’t know the answer." if language == "en" else "माफ गर्नुहोस्, म तपाईंको प्रश्नको जवाफ दिन सक्दिन।"
    else:
        bot_reply = answers[best_idx]
        # Translate to Nepali if requested
        if language == "ne" and Translator:
            try:
                translator = Translator(to_lang="ne")
                bot_reply = translator.translate(bot_reply)
            except Exception:
                pass  # fallback to English if translation fails

    return jsonify({"answer": bot_reply})

# -------------------
# Run the server
# -------------------
if __name__ == "__main__":
    app.run(debug=True)

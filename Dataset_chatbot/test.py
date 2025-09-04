import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------
# Load the PKL file
# ------------------------
with open("question_embeddings.pkl", "rb") as f:
    questions, answers, embeddings = pickle.load(f)

# Ensure embeddings is a numpy array
embeddings = np.array(embeddings)

print(f"Loaded {len(questions)} questions and {len(answers)} answers.")
print(f"Embeddings shape: {embeddings.shape}")

# Load the same model you use in Flask
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# ------------------------
# Test some sample questions
# ------------------------
sample_questions = [
    "What is fertilizer?",
    "How do I plant rice?",
    "पानी कहिले हाल्ने?"  # Nepali example
]

threshold = 0.55  # same as your Flask code

for q in sample_questions:
    query_embedding = model.encode([q])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]

    print("\nQuestion:", q)
    print("Best similarity score:", best_score)

    if best_score < threshold:
        print("Bot reply: माफ गर्नुहोस्, म तपाईंको प्रश्नको जवाफ अहिले दिन सक्दिन।")
    else:
        print("Bot reply:", answers[best_idx])

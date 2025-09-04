from sentence_transformers import SentenceTransformer
import csv
import pickle

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

questions = []
embeddings = []

with open("bilingual_dataset.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        q_en = row["question_en"].strip()
        q_ne = row["question_ne"].strip()

        if q_en and q_en != "Error":
            questions.append(q_en)
            embeddings.append(model.encode(q_en))

        if q_ne and q_ne != "Error":
            questions.append(q_ne)
            embeddings.append(model.encode(q_ne))

# Save to pickle
with open("question_embeddings.pkl", "wb") as f:
    pickle.dump((questions, embeddings), f)
    print("✅ Embeddings generated and saved to question_embeddings.pkl")


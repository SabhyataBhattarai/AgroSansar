from sentence_transformers import SentenceTransformer
import csv
import pickle
import re

def preprocess_text(text):
    return re.sub(r"[^\w\s]", "", text.lower().strip())

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

questions = []
with open("bilingual_dataset_final.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        questions.append(preprocess_text(row["question_en"]))  # preprocess all

embeddings = model.encode(questions)

with open("question_embeddings.pkl", "wb") as f:
    pickle.dump((questions, embeddings), f)

print(f"✅ Embeddings generated for {len(questions)} questions and saved.")

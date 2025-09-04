from datasets import load_dataset
from translate import Translator
import csv
import os

# Load dataset
dataset = load_dataset("KisanVaani/agriculture-qa-english-only")
total_records = len(dataset["train"])
print(f"Total samples available: {total_records}")
print("Sample structure:", dataset["train"][0])

# Setup translator
translator = Translator(to_lang="ne")

# Start from 0 this time (load all questions)
start_index = 0
csv_file = "bilingual_dataset.csv"

# Open CSV in append mode
header_needed = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if header_needed:
        writer.writerow(["question_en", "answer_en", "question_ne", "answer_ne"])

    for i in range(start_index, total_records):
        q_en = dataset["train"][i]["question"]
        a_en = dataset["train"][i]["answers"]

        try:
            q_ne = translator.translate(q_en)
            a_ne = translator.translate(a_en)

            if "MYMEMORY WARNING" in q_ne or "MYMEMORY WARNING" in a_ne:
                print("\n🚫 Translation quota reached. Halting translation.")
                break

            writer.writerow([q_en, a_en, q_ne, a_ne])
            print(f"\n✅ Sample {i + 1}")
            print("Q (EN):", q_en)
            print("A (EN):", a_en)
            print("Q (NE):", q_ne)
            print("A (NE):", a_ne)

        except Exception as e:
            print(f"⚠️ Error at sample {i}: {e}")

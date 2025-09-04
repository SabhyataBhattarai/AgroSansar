import csv

def generate_paraphrases(question):
    patterns = [
        ("when should", "what is the right time to"),
        ("how do I", "what’s the way to"),
        ("what is", "could you tell me what"),
        ("why is", "what’s the reason for"),
        ("how can I", "what’s the method to"),
        ("best way to", "recommended method to"),
        ("should I", "is it necessary to"),
        ("how much", "what quantity of"),
    ]
    question = question.lower()
    paraphrased = []

    for original, replacement in patterns:
        if original in question:
            new_q = question.replace(original, replacement)
            if new_q != question:
                paraphrased.append(new_q.capitalize())
    return paraphrased

input_file = "bilingual_dataset.csv"
output_file = "bilingual_dataset_augmented.csv"

with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    count = 0
    for row in reader:
        writer.writerow(row)
        count += 1

        alt_phrases = generate_paraphrases(row["question_en"])
        for alt in alt_phrases:
            new_row = {
                "question_en": alt,
                "answer_en": row["answer_en"],
                "question_ne": "N/A",
                "answer_ne": row["answer_ne"]
            }
            writer.writerow(new_row)
            count += 1

print(f"✅ Dataset augmented with paraphrases. Total rows: {count}")

import csv
from difflib import get_close_matches

# Load bilingual dataset
qa_pairs = []
with open("bilingual_dataset.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        qa_pairs.append({
            "question_en": row["question_en"],
            "question_ne": row["question_ne"],
            "answer_ne": row["answer_ne"]
        })

print("✅ Bilingual dataset loaded successfully.")

def find_answer_en_input(user_input):
    # Match user input to English questions
    questions = [pair["question_en"] for pair in qa_pairs]
    matches = get_close_matches(user_input, questions, n=1, cutoff=0.6)

    if matches:
        matched_q = matches[0]
        for pair in qa_pairs:
            if pair["question_en"] == matched_q:
                return pair["question_ne"], pair["answer_ne"]
    return None, None

# Chat loop
print("\n🤖 Type your question in English (testing mode). Type 'exit' to quit.")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Bot: बाइ बाइ! 👋")
        break

    matched_q, answer = find_answer_en_input(user_input)
    if answer:
        print(f"Bot (matched Nepali): {matched_q}")
        print(f"Bot (answer in Nepali): {answer}")
    else:
        print("Bot: क्षमा गर्नुहोस्, मैले त्यो प्रश्न बुझिन। 🙏")

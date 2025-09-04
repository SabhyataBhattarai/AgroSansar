from sentence_transformers import SentenceTransformer, util
import pickle
import re
import csv
import speech_recognition as sr
import pyttsx3

# ------------------ Voice Engine Setup ------------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speaking speed
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Default voice

def speak(text):
    print("🔊 Speaking...")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ बोल्नुहोस् (Speak now)...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language="ne-NP")
        print("तपाईं:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("😕 आवाज बुझ्न सकिएन। फेरि प्रयास गर्नुहोस्।")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ API Error: {e}")
        return ""

# ------------------ Load Embeddings & Answers ------------------
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

with open("question_embeddings.pkl", "rb") as f:
    questions, embeddings = pickle.load(f)

answers_map = {}
with open("bilingual_dataset.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        answers_map[row["question_en"]] = row["answer_ne"] if row["answer_ne"] != "Error" else row["answer_en"]

# ------------------ Preprocessing ------------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text

# ------------------ Chat Function ------------------
def chatbot(query):
    cleaned_query = preprocess(query)
    query_embedding = model.encode(cleaned_query)
    similarity_scores = util.cos_sim(query_embedding, embeddings)[0]
    best_score, best_idx = similarity_scores.max().item(), similarity_scores.argmax().item()

    print(f"🔎 Best match score: {best_score:.2f}")
    threshold = 0.65

    if best_score >= threshold:
        matched_question = questions[best_idx]
        return answers_map.get(matched_question, "माफ गर्नुहोस्, म त्यो बुझिन।")
    else:
        return "माफ गर्नुहोस्, म त्यो बुझिन। कृपया प्रश्नलाई फरक तरिकाले राख्न सक्नुहुन्छ?"

# ------------------ Main Chat Loop ------------------
if __name__ == "__main__":
    print("🚜 कृषि सल्लाहकार बोट तयार छ! (Type 'exit' to quit)")
    mode = input("🔧 Text वा Voice? (T/V): ").strip().lower()

    while True:
        if mode == "v":
            user_input = listen()
            if not user_input:
                continue
            if "exit" in user_input.lower():
                break
        else:
            user_input = input("\nतपाईं: ")
            if user_input.lower() == "exit":
                break

        response = chatbot(user_input)
        print("बोट:", response)
        speak(response)

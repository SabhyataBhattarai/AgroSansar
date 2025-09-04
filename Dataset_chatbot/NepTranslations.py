from translate import Translator
import csv

translator = Translator(to_lang="ne")
input_file = "bilingual_dataset_augmented.csv"
output_file = "bilingual_dataset_final.csv"

with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    count = 0
    translated = 0

    for row in reader:
        if row["question_ne"].strip().upper() == "N/A":
            try:
                row["question_ne"] = translator.translate(row["question_en"])
                translated += 1
            except Exception as e:
                print(f"Translation failed for: {row['question_en']} - {e}")
                row["question_ne"] = "Translation Error"

        writer.writerow(row)
        count += 1

print(f"✅ Finished! Translated {translated} new questions out of {count} rows.")
print(f"📝 Final dataset saved to: {output_file}")

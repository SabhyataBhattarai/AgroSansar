import pickle

with open("question_embeddings.pkl", "rb") as f:
    data = pickle.load(f)

# Check the structure
if isinstance(data, tuple):
    print("Tuple contains:", [type(item) for item in data])
    for i, item in enumerate(data):
        print(f"\nItem {i} Preview:")
        if isinstance(item, list):
            print(item[:5])  # Show first 5 entries
        else:
            print(item)
else:
    print("Unexpected format:", type(data))

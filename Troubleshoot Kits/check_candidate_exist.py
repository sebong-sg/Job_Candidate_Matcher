from chromadb import PersistentClient

client = PersistentClient(path="./chroma_db")
collection = client.get_collection(name="candidates")

records = collection.get(include=["metadatas"])

found = False
for i, meta in enumerate(records["metadatas"]):
    if meta.get("name") == "Peter Tan":
        print(f"Found Peter Tan with ID: {records['ids'][i]}")
        found = True

if not found:
    print("Peter Tan not found in candidates collection.")

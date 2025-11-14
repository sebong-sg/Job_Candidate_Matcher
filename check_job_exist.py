from chromadb import PersistentClient

client = PersistentClient(path="./chroma_db")
jobs = client.get_collection(name="jobs")

records = jobs.get(include=["metadatas"])

found = False
for i, meta in enumerate(records["metadatas"]):
    if meta.get("title") == "Python Code Developer 2":  # Replace with your actual job title
        print(f"Found job with ID: {records['ids'][i]}")
        found = True

if not found:
    print("Job not found.")

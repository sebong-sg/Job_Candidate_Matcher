from chromadb import PersistentClient

client = PersistentClient(path="./chroma_db")
collection = client.get_collection(name="candidates")

collection.delete(ids=["5"])
print("Deleted candidate with ID: 5")

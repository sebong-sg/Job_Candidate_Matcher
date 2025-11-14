#!/usr/bin/env python3
import sys
from chromadb import PersistentClient

# to involke python preview_delete_candidates.py "candidate_name"

def preview_candidates_by_name(collection_name, name_search):
    """Preview candidates that match the name before deleting"""
    client = PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=collection_name)
    
    # Get all records to search through
    all_records = collection.get(include=["metadatas", "documents"])
    
    matching_records = []
    
    print(f"🔍 SEARCHING FOR CANDIDATES WITH NAME: '{name_search}'")
    print("=" * 60)
    
    for i, metadata in enumerate(all_records["metadatas"]):
        candidate_name = metadata.get("name", "")
        if name_search.lower() in candidate_name.lower():
            record_data = {
                "id": all_records["ids"][i],
                "name": candidate_name,
                "metadata": metadata,
                "document": all_records["documents"][i] if all_records.get('documents') else None
            }
            matching_records.append(record_data)
    
    if matching_records:
        print(f"📋 Found {len(matching_records)} matching candidates:")
        for record in matching_records:
            print(f"\n🎯 ID: {record['id']}")
            print(f"   Name: {record['name']}")
            print(f"   Email: {record['metadata'].get('email', 'N/A')}")
            print(f"   Location: {record['metadata'].get('location', 'N/A')}")
            if record['document']:
                print(f"   Preview: {record['document'][:150]}...")
        
        # Ask for confirmation
        response = input(f"\n❓ Delete these {len(matching_records)} candidates? (y/N): ")
        if response.lower() == 'y':
            ids_to_delete = [record['id'] for record in matching_records]
            collection.delete(ids=ids_to_delete)
            print(f"✅ Deleted {len(ids_to_delete)} candidates")
        else:
            print("❌ Deletion cancelled")
    else:
        print(f"❌ No candidates found with name containing: '{name_search}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python preview_candidates.py <name_to_search>")
        print("Example: python preview_candidates.py 'Peter'")
        sys.exit(1)
    
    name_to_search = sys.argv[1]
    preview_candidates_by_name("candidates", name_to_search)
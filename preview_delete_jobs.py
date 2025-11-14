#!/usr/bin/env python3
import sys
from chromadb import PersistentClient

def preview_jobs_by_title(collection_name, title_search):
    """Preview jobs that match the title before deleting"""
    client = PersistentClient(path="./chroma_db")
    collection = client.get_collection(name=collection_name)
    
    # Get all records to search through
    all_records = collection.get(include=["metadatas", "documents"])
    
    matching_records = []
    
    print(f"🔍 SEARCHING FOR JOBS WITH TITLE: '{title_search}'")
    print("=" * 60)
    
    for i, metadata in enumerate(all_records["metadatas"]):
        job_title = metadata.get("title", "")
        if title_search.lower() in job_title.lower():
            record_data = {
                "id": all_records["ids"][i],
                "title": job_title,
                "metadata": metadata,
                "document": all_records["documents"][i] if all_records.get('documents') else None
            }
            matching_records.append(record_data)
    
    if matching_records:
        print(f"📋 Found {len(matching_records)} matching jobs:")
        for record in matching_records:
            print(f"\n🎯 ID: {record['id']}")
            print(f"   Title: {record['title']}")
            print(f"   Company: {record['metadata'].get('company', 'N/A')}")
            print(f"   Location: {record['metadata'].get('location', 'N/A')}")
            print(f"   Experience: {record['metadata'].get('experience_required', 'N/A')} years")
            if record['document']:
                print(f"   Preview: {record['document'][:150]}...")
        
        # Ask for confirmation
        response = input(f"\n❓ Delete these {len(matching_records)} jobs? (y/N): ")
        if response.lower() == 'y':
            ids_to_delete = [record['id'] for record in matching_records]
            collection.delete(ids=ids_to_delete)
            print(f"✅ Deleted {len(ids_to_delete)} jobs")
        else:
            print("❌ Deletion cancelled")
    else:
        print(f"❌ No jobs found with title containing: '{title_search}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python preview_jobs.py <title_to_search>")
        print("Example: python preview_jobs.py 'Python Developer'")
        print("Example: python preview_jobs.py 'Senior'")
        print("Example: python preview_jobs.py 'Code Developer'")
        sys.exit(1)
    
    title_to_search = sys.argv[1]
    preview_jobs_by_title("jobs", title_to_search)
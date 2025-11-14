import sqlite3
import json

def check_existence():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 CHECKING IF PETER TAN AND JOB EXIST IN DATABASE")
    print("=" * 60)
    
    # Get all names and titles
    cursor.execute("""
        SELECT em.key, em.string_value, e.embedding_id
        FROM embedding_metadata em
        JOIN embeddings e ON em.id = e.embedding_id
        WHERE em.key IN ('name', 'title')
        ORDER BY e.embedding_id;
    """)
    
    results = cursor.fetchall()
    
    print("👥 ALL CANDIDATES:")
    candidates = [r for r in results if r[0] == 'name']
    for key, name, embedding_id in candidates:
        print(f"  {embedding_id}: {name}")
        if 'Peter Tan' in name:
            print(f"    ✅ PETER TAN FOUND! ID: {embedding_id}")
    
    print("\n💼 ALL JOBS:")
    jobs = [r for r in results if r[0] == 'title']  
    for key, title, embedding_id in jobs:
        print(f"  {embedding_id}: {title}")
        if 'Senior Python Code Developer' in title:
            print(f"    ✅ JOB FOUND! ID: {embedding_id}")
    
    # Check total counts
    print(f"\n📊 DATABASE SUMMARY:")
    print(f"  Total candidates: {len(candidates)}")
    print(f"  Total jobs: {len(jobs)}")
    
    conn.close()

if __name__ == "__main__":
    check_existence()

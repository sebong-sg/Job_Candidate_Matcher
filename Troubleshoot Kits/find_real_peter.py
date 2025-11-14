import sqlite3
import json

def find_real_peter():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 FINDING REAL PETER TAN CANDIDATE")
    print("=" * 50)
    
    # Find ALL candidates (names)
    cursor.execute("""
        SELECT em.id, em.string_value
        FROM embedding_metadata em
        WHERE em.key = 'name'
        ORDER BY em.id;
    """)
    
    candidates = cursor.fetchall()
    print("👥 ALL CANDIDATES:")
    for candidate_id, name in candidates:
        print(f"  ID {candidate_id}: {name}")
        if 'Peter Tan' in name:
            print(f"    ✅ THIS IS PETER TAN!")
    
    # Now check the latest candidate (should be Alex Chen or Peter Tan)
    print(f"\n🎯 CHECKING LATEST CANDIDATES:")
    cursor.execute("""
        SELECT em.id, em.key, em.string_value
        FROM embedding_metadata em
        JOIN embeddings e ON em.id = e.embedding_id
        WHERE em.key = 'name'
        ORDER BY e.created_at DESC
        LIMIT 5;
    """)
    
    latest = cursor.fetchall()
    for candidate_id, key, name in latest:
        print(f"  ID {candidate_id}: {name}")
        if 'Peter Tan' in name:
            print(f"    🎯 FOUND PETER TAN!")
            
            # Check his cultural attributes
            cursor.execute("""
                SELECT string_value FROM embedding_metadata 
                WHERE id = ? AND key = 'cultural_attributes';
            """, (candidate_id,))
            
            cultural_result = cursor.fetchone()
            if cultural_result:
                cultural_data = json.loads(cultural_result[0])
                print(f"    🎭 CULTURAL ATTRIBUTES: {cultural_data}")
            else:
                print(f"    ❌ NO CULTURAL ATTRIBUTES")
    
    conn.close()

if __name__ == "__main__":
    find_real_peter()

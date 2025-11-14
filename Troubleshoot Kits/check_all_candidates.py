import sqlite3
import json

def check_all_candidates():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 CHECKING ALL CANDIDATES AND THEIR CULTURAL ATTRIBUTES")
    print("=" * 60)
    
    # Get all candidates
    cursor.execute("""
        SELECT em.id, em.string_value
        FROM embedding_metadata em
        WHERE em.key = 'name'
        ORDER BY em.id;
    """)
    
    candidates = cursor.fetchall()
    
    print("👥 ALL CANDIDATES:")
    candidate_data = {}
    for candidate_id, name in candidates:
        print(f"  ID {candidate_id}: {name}")
        
        # Get cultural attributes for this candidate
        cursor.execute("""
            SELECT string_value FROM embedding_metadata 
            WHERE id = ? AND key = 'cultural_attributes';
        """, (candidate_id,))
        
        cultural_result = cursor.fetchone()
        if cultural_result:
            cultural_data = json.loads(cultural_result[0])
            candidate_data[candidate_id] = {'name': name, 'cultural': cultural_data}
            print(f"    🎭 Cultural: {cultural_data}")
        else:
            print(f"    ❌ No cultural attributes")
    
    conn.close()
    return candidate_data

if __name__ == "__main__":
    check_all_candidates()

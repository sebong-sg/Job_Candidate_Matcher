import sqlite3
import json

def verify_new_candidate():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 VERIFYING NEW CANDIDATE HAS CULTURAL ATTRIBUTES")
    print("=" * 60)
    
    # Find Alex Chen
    cursor.execute("""
        SELECT em.id, em.key, em.string_value
        FROM embedding_metadata em
        WHERE em.string_value LIKE '%Alex Chen%'
        OR em.string_value LIKE '%alex.chen@email.com%';
    """)
    
    results = cursor.fetchall()
    
    alex_id = None
    for row in results:
        metadata_id, key, string_value = row
        if key == 'name' and 'Alex Chen' in string_value:
            alex_id = metadata_id
            print(f"✅ Found Alex Chen with ID: {alex_id}")
            break
    
    if alex_id:
        # Check for cultural attributes
        cursor.execute("""
            SELECT key, string_value 
            FROM embedding_metadata 
            WHERE id = ? AND key = 'cultural_attributes';
        """, (alex_id,))
        
        cultural_result = cursor.fetchone()
        if cultural_result:
            key, cultural_json = cultural_result
            print(f"🎭 CULTURAL ATTRIBUTES FOUND: {cultural_json}")
            try:
                cultural_data = json.loads(cultural_json)
                print(f"   Parsed: {cultural_data}")
            except:
                print("   Could not parse JSON")
        else:
            print("❌ NO CULTURAL ATTRIBUTES FOUND - FIX DIDN'T WORK")
    else:
        print("❌ Alex Chen not found in database")
    
    conn.close()

if __name__ == "__main__":
    verify_new_candidate()

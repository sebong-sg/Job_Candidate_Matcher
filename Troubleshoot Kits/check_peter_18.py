import sqlite3
import json

def check_peter_18():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 CHECKING PETER TAN ID 18")
    print("=" * 50)
    
    # Get ALL metadata for ID 18
    cursor.execute("""
        SELECT key, string_value 
        FROM embedding_metadata 
        WHERE id = 18
        ORDER BY key;
    """)
    
    results = cursor.fetchall()
    print(f"📋 ALL METADATA FOR PETER TAN (ID 18):")
    
    cultural_found = False
    for key, string_value in results:
        print(f"  {key}: {string_value}")
        
        if key == 'cultural_attributes' and string_value:
            cultural_found = True
            try:
                cultural_data = json.loads(string_value)
                print(f"    🎭 PARSED CULTURAL: {cultural_data}")
            except:
                print(f"    ❌ Could not parse cultural attributes")
    
    if not cultural_found:
        print("❌ NO CULTURAL ATTRIBUTES FOUND FOR PETER TAN ID 18")
    
    conn.close()

if __name__ == "__main__":
    check_peter_18()

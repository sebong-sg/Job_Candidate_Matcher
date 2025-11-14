import sqlite3
import json

def debug_peter_7():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 DEBUG PETER TAN ID 7 COMPLETELY")
    print("=" * 50)
    
    # Get ALL metadata for ID 7
    cursor.execute("""
        SELECT key, string_value 
        FROM embedding_metadata 
        WHERE id = 7
        ORDER BY key;
    """)
    
    results = cursor.fetchall()
    print(f"📋 ALL METADATA FOR ID 7:")
    
    for key, string_value in results:
        print(f"  {key}: {string_value}")
        
        if key == 'cultural_attributes' and string_value:
            try:
                cultural_data = json.loads(string_value)
                print(f"    🎭 PARSED CULTURAL: {cultural_data}")
            except:
                print(f"    ❌ Could not parse cultural attributes")
    
    conn.close()

if __name__ == "__main__":
    debug_peter_7()

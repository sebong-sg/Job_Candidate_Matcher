import sqlite3
import json

def examine_peter_tan():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 EXAMINING PETER TAN (ID: 5) COMPLETELY")
    print("=" * 60)
    
    # Get ALL metadata for embedding ID 5
    cursor.execute("""
        SELECT key, string_value, int_value, float_value, bool_value
        FROM embedding_metadata 
        WHERE id = 5
        ORDER BY key;
    """)
    
    results = cursor.fetchall()
    print(f"📋 ALL METADATA FOR PETER TAN (ID 5):")
    
    cultural_attributes_found = False
    for key, string_value, int_val, float_val, bool_val in results:
        print(f"  {key}: {string_value or int_val or float_val or bool_val}")
        
        if key == 'cultural_attributes' and string_value:
            cultural_attributes_found = True
            try:
                cultural_data = json.loads(string_value)
                print(f"    🎭 PARSED CULTURAL ATTRIBUTES: {cultural_data}")
            except:
                print(f"    ❌ Could not parse cultural attributes")
    
    if not cultural_attributes_found:
        print("  ❌ NO CULTURAL ATTRIBUTES FOUND FOR PETER TAN")
    
    # Also check the job (ID 14 from earlier)
    print(f"\n🔍 EXAMINING JOB (ID: 14) COMPLETELY:")
    cursor.execute("""
        SELECT key, string_value, int_value, float_value, bool_value
        FROM embedding_metadata 
        WHERE id = 14
        ORDER BY key;
    """)
    
    job_results = cursor.fetchall()
    job_cultural_found = False
    for key, string_value, int_val, float_val, bool_val in job_results:
        print(f"  {key}: {string_value or int_val or float_val or bool_val}")
        
        if key == 'cultural_attributes' and string_value:
            job_cultural_found = True
            try:
                cultural_data = json.loads(string_value)
                print(f"    🎭 PARSED CULTURAL ATTRIBUTES: {cultural_data}")
            except:
                print(f"    ❌ Could not parse cultural attributes")
    
    if not job_cultural_found:
        print("  ❌ NO CULTURAL ATTRIBUTES FOUND FOR JOB")
    
    conn.close()

if __name__ == "__main__":
    examine_peter_tan()

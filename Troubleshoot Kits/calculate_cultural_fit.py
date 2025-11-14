import sqlite3
import json

def calculate_peter_tan_fit():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 CALCULATING PETER TAN'S CULTURAL FIT SCORE")
    print("=" * 60)
    
    # Get Peter Tan's cultural attributes
    cursor.execute("""
        SELECT string_value FROM embedding_metadata 
        WHERE id = 7 AND key = 'cultural_attributes';
    """)
    
    peter_result = cursor.fetchone()
    if not peter_result:
        print("❌ Peter Tan cultural attributes not found")
        return
    
    peter_cultural = json.loads(peter_result[0])
    print(f"👤 PETER TAN CULTURAL: {peter_cultural}")
    
    # Get Job's cultural attributes (ID 14)
    cursor.execute("""
        SELECT string_value FROM embedding_metadata 
        WHERE id = 14 AND key = 'cultural_attributes';
    """)
    
    job_result = cursor.fetchone()
    if not job_result:
        print("❌ Job cultural attributes not found")
        return
    
    job_cultural = json.loads(job_result[0])
    print(f"💼 JOB CULTURAL: {job_cultural}")
    
    # Calculate cultural fit manually
    print(f"\n🎯 CALCULATING CULTURAL FIT:")
    total_score = 0
    count = 0
    
    for attr in ['teamwork', 'innovation', 'work_environment', 'work_pace', 'customer_focus']:
        # Job stores as (score, confidence), candidate stores as raw score
        job_score = job_cultural[attr][0] if isinstance(job_cultural[attr], list) else job_cultural[attr]
        candidate_score = peter_cultural[attr]
        
        compatibility = 1 - abs(job_score - candidate_score)
        total_score += compatibility
        count += 1
        
        print(f"   {attr.upper():<18} Job: {job_score:.2f} | Peter: {candidate_score:.2f} | Fit: {compatibility:.2f}")
    
    final_score = total_score / count if count > 0 else 0.5
    print(f"\n📊 FINAL CULTURAL FIT SCORE: {final_score:.2f} ({final_score*100:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    calculate_peter_tan_fit()

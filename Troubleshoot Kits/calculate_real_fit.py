import sqlite3
import json

def calculate_real_fit():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🔍 CALCULATING REAL CULTURAL FIT SCORE")
    print("=" * 60)
    
    # Get Peter Tan's cultural attributes (ID 18)
    cursor.execute("SELECT string_value FROM embedding_metadata WHERE id = 18 AND key = 'cultural_attributes';")
    peter_result = cursor.fetchone()
    peter_cultural = json.loads(peter_result[0]) if peter_result else {}
    print(f"👤 PETER TAN CULTURAL: {peter_cultural}")
    
    # Get Job's cultural attributes (ID 14)
    cursor.execute("SELECT string_value FROM embedding_metadata WHERE id = 14 AND key = 'cultural_attributes';")
    job_result = cursor.fetchone()
    job_cultural = json.loads(job_result[0]) if job_result else {}
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
    
    # Compare with the displayed 81%
    displayed_score = 0.81
    difference = abs(final_score - displayed_score)
    print(f"\n🔍 COMPARISON WITH DISPLAYED 81%:")
    print(f"   Calculated: {final_score:.2f} ({final_score*100:.1f}%)")
    print(f"   Displayed:  {displayed_score:.2f} ({displayed_score*100:.1f}%)")
    print(f"   Difference: {difference:.2f} ({difference*100:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    calculate_real_fit()

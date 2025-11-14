import sqlite3
import json

def calculate_all_scores():
    conn = sqlite3.connect('chroma_db/chroma.sqlite3')
    cursor = conn.cursor()
    
    print("🎯 CALCULATING CULTURAL FIT SCORES FOR ALL CANDIDATES")
    print("=" * 60)
    
    # Get the job (ID 14)
    cursor.execute("SELECT string_value FROM embedding_metadata WHERE id = 14 AND key = 'cultural_attributes';")
    job_result = cursor.fetchone()
    if not job_result:
        print("❌ Job cultural attributes not found")
        return
    
    job_cultural = json.loads(job_result[0])
    print(f"💼 JOB: Senior Python Code Developer")
    print(f"   Cultural: {job_cultural}")
    print()
    
    # Get all candidates
    cursor.execute("""
        SELECT em.id, em.string_value
        FROM embedding_metadata em
        WHERE em.key = 'name'
        ORDER BY em.id;
    """)
    
    candidates = cursor.fetchall()
    
    print("📊 CULTURAL FIT SCORES:")
    print("-" * 50)
    
    scores = []
    for candidate_id, name in candidates:
        # Get cultural attributes for this candidate
        cursor.execute("""
            SELECT string_value FROM embedding_metadata 
            WHERE id = ? AND key = 'cultural_attributes';
        """, (candidate_id,))
        
        cultural_result = cursor.fetchone()
        if not cultural_result:
            continue
            
        candidate_cultural = json.loads(cultural_result[0])
        
        # Calculate cultural fit
        total_score = 0
        count = 0
        
        for attr in ['teamwork', 'innovation', 'work_environment', 'work_pace', 'customer_focus']:
            # Job stores as (score, confidence), candidate stores as raw score
            job_score = job_cultural[attr][0] if isinstance(job_cultural[attr], list) else job_cultural[attr]
            candidate_score = candidate_cultural[attr]
            
            compatibility = 1 - abs(job_score - candidate_score)
            total_score += compatibility
            count += 1
        
        final_score = total_score / count if count > 0 else 0.5
        scores.append((name, final_score, candidate_id))
        
        print(f"👤 {name:<15} (ID: {candidate_id}): {final_score:.1%}")
    
    # Sort by score
    scores.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🏆 TOP CANDIDATES FOR SENIOR PYTHON DEVELOPER:")
    print("-" * 50)
    for name, score, candidate_id in scores[:5]:
        print(f"  {name:<15}: {score:.1%} (ID: {candidate_id})")
    
    conn.close()

if __name__ == "__main__":
    calculate_all_scores()

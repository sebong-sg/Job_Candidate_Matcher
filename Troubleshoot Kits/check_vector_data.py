import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from vector_db import vector_db
from chroma_data_manager import ChromaDataManager

def check_vector_data():
    print("🔍 CHECKING VECTOR DATABASE DATA STRUCTURE")
    print("=" * 50)
    
    db = ChromaDataManager()
    
    # Get candidates from both sources
    candidates_db = db.load_candidates()
    print(f"📁 Candidates from ChromaDataManager: {len(candidates_db)}")
    
    # Check vector DB directly
    vector_count = vector_db.get_candidate_count()
    print(f"📊 Candidates in Vector DB: {vector_count}")
    
    # Compare first candidate from both sources
    if candidates_db:
        sample_candidate = candidates_db[0]
        print(f"\n📋 SAMPLE CANDIDATE DATA STRUCTURE:")
        for key, value in sample_candidate.items():
            print(f"   {key}: {type(value)} = {value}")
        
        # Check if this candidate exists in vector DB
        print(f"\n🔍 CHECKING VECTOR DB FOR '{sample_candidate.get('name')}':")
        try:
            # Try to find this candidate in vector DB
            results = vector_db.semantic_search({"description": sample_candidate.get('profile', '')}, limit=1)
            if results:
                print(f"✅ Found in vector DB: {results[0].get('name')}")
            else:
                print("❌ Not found in vector DB")
        except Exception as e:
            print(f"❌ Search error: {e}")
    
    # Check if the issue is with the vector_db.add_candidate method
    print(f"\n🧪 TESTING VECTOR DB ADD METHOD:")
    try:
        # Test with minimal candidate data
        test_candidate = {
            "name": "Test Candidate",
            "profile": "Test profile for debugging",
            "skills": ["python", "debugging"]
        }
        success = vector_db.add_candidate(test_candidate)
        print(f"✅ Add candidate test: {success}")
    except Exception as e:
        print(f"❌ Add candidate error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_vector_data()

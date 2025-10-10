# 🧪 TESTING FILE
# This file checks if our main program works correctly

import sys
import os

# Add src folder to Python path so we can import our matcher
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from matcher import SimpleMatcher

def test_basic_matching():
    """Test if our matcher finds basic matches"""
    print("🧪 Running basic matching test...")
    
    # Create matcher
    matcher = SimpleMatcher()
    
    # Test data
    test_jobs = ["Python developer needed"]
    test_candidates = ["I know Python programming"]
    
    # Test matching
    results = matcher.find_matches(test_jobs, test_candidates)
    
    # Check if we got results
    assert len(results) > 0, "❌ No matches found!"
    assert 0 in results, "❌ Job 0 not in results!"
    
    print("✅ Basic matching test passed!")

def test_empty_data():
    """Test with empty data"""
    print("🧪 Running empty data test...")
    
    matcher = SimpleMatcher()
    results = matcher.find_matches([], [])
    
    assert results == {}, "❌ Empty data should return empty results!"
    print("✅ Empty data test passed!")

if __name__ == "__main__":
    print("🚀 STARTING TESTS")
    print("=" * 40)
    
    test_basic_matching()
    test_empty_data()
    
    print("=" * 40)
    print("🎉 ALL TESTS PASSED! Your matcher is working correctly.")
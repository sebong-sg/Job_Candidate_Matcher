"""
🎯 PROFILE RELEVANCE ANALYZER - Pure Semantic Understanding
Measures contextual fit between job descriptions and candidate profiles
"""

from semantic_matcher import semantic_matcher

class ProfileRelevanceAnalyzer:
    def __init__(self):
        print("✅ Profile Relevance Analyzer initialized with semantic matching!")
    
    def calculate_semantic_relevance(self, job_description, candidate_profile):
        """
        Calculate pure semantic relevance using advanced embeddings
        Measures how well the candidate's profile contextually fits the job description
        """
        if not job_description or not candidate_profile:
            return 0.5  # Neutral for missing data
        
        # Use semantic matching for true understanding
        semantic_score = semantic_matcher.calculate_similarity(
            job_description, 
            candidate_profile
        )
        
        print(f"🔍 Semantic Relevance: {semantic_score:.1%}")
        print(f"   Job: {job_description[:60]}...")
        print(f"   Candidate: {candidate_profile[:60]}...")
        
        return semantic_score

# Global instance for reuse
profile_analyzer = ProfileRelevanceAnalyzer()
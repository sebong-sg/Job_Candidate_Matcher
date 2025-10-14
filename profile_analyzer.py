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

    # 🆕 CAREER TRAJECTORY ANALYSIS
    def analyze_career_trajectory(self, candidate_profile, candidate_experience):
        """Evaluate career growth potential"""
        profile_text = candidate_profile.lower()
        
        growth_score = 0.5  # Base score
        
        # Promotion indicators
        promotion_indicators = ['promoted', 'advanced to', 'grown into', 'progressed to']
        if any(indicator in profile_text for indicator in promotion_indicators):
            growth_score += 0.2
        
        # Leadership indicators (even in non-manager roles)
        leadership_indicators = ['led', 'mentored', 'guided', 'coordinated', 'spearheaded']
        leadership_count = sum(1 for indicator in leadership_indicators if indicator in profile_text)
        growth_score += leadership_count * 0.05
        
        # Skill expansion indicators
        skill_verbs = ['learned', 'mastered', 'developed skills in', 'expanded into']
        if any(verb in profile_text for verb in skill_verbs):
            growth_score += 0.15
        
        # Experience quality weighting
        if candidate_experience >= 8:
            growth_score += 0.1  # Senior candidates expected to show growth
        
        return min(1.0, growth_score)

# Global instance for reuse
profile_analyzer = ProfileRelevanceAnalyzer()
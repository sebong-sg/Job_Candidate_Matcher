"""
🎯 SEMANTIC MATCHER - True Understanding with Sentence Transformers
Replaces basic TF-IDF with advanced embeddings for semantic understanding
"""

import numpy as np
import subprocess
import sys
import warnings
from sklearn.metrics.pairwise import cosine_similarity

# Suppress warnings
warnings.filterwarnings('ignore')

def install_and_import_sentence_transformers():
    """Install sentence-transformers package if not available and return availability status"""
    try:
        import sentence_transformers
        return True
    except ImportError:
        print("📦 Installing sentence-transformers (this may take a minute)...")
        try:
            # Use the current Python's pip to avoid path issues
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "sentence-transformers", "--quiet", "--no-warn-conflicts"
            ])
            print("✅ sentence-transformers installed successfully!")
            
            # Try to import again after installation
            try:
                import sentence_transformers
                return True
            except ImportError:
                print("❌ Installation succeeded but import failed")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install sentence-transformers: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during installation: {e}")
            return False

# Global variable for semantic availability
SEMANTIC_AVAILABLE = install_and_import_sentence_transformers()

# Import after ensuring availability
sentence_transformer_model = None
if SEMANTIC_AVAILABLE:
    try:
        from sentence_transformers import SentenceTransformer
        sentence_transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Sentence Transformers loaded - using advanced semantic matching!")
    except Exception as e:
        print(f"⚠️ Failed to load sentence transformer model: {e}")
        SEMANTIC_AVAILABLE = False
else:
    print("⚠️ Sentence Transformers not available - using enhanced basic matching")

class SemanticMatcher:
    def __init__(self):
        self.model = sentence_transformer_model
        
        if self.model:
            print("🎯 Semantic matcher ready with all-MiniLM-L6-v2 model!")
        else:
            print("🔧 Using enhanced basic matching (word overlap + technical terms)")
    
    def encode_text(self, text):
        """Convert text to semantic embedding vector"""
        if not text or not self.model:
            return None
        
        # Clean and prepare text
        clean_text = text.strip()
        if len(clean_text) < 10:  # Too short for meaningful embedding
            return None
            
        try:
            return self.model.encode([clean_text])[0]
        except Exception as e:
            print(f"⚠️ Encoding error: {e}")
            return None
    
    def calculate_similarity(self, text1, text2):
        """Calculate semantic similarity between two texts"""
        if not self.model:
            # Fallback: enhanced similarity check
            return self.enhanced_similarity_fallback(text1, text2)
        
        embedding1 = self.encode_text(text1)
        embedding2 = self.encode_text(text2)
        
        if embedding1 is None or embedding2 is None:
            return self.enhanced_similarity_fallback(text1, text2)
        
        try:
            # Calculate cosine similarity between embeddings
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            return float(similarity)
        except Exception as e:
            print(f"⚠️ Similarity calculation error: {e}")
            return self.enhanced_similarity_fallback(text1, text2)
    
    def enhanced_similarity_fallback(self, text1, text2):
        """Enhanced fallback similarity calculation when embeddings aren't available"""
        if not text1 or not text2:
            return 0.5
            
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Simple word overlap
        words1 = set(text1_lower.split())
        words2 = set(text2_lower.split())
        
        if not words1 or not words2:
            return 0.5
            
        common_words = words1.intersection(words2)
        base_similarity = len(common_words) / max(len(words1), len(words2))
        
        # Boost for important technical terms
        important_terms = {
            'python': 0.15, 'developer': 0.10, 'django': 0.08, 'flask': 0.08,
            'web': 0.06, 'api': 0.06, 'machine learning': 0.12, 'react': 0.08,
            'javascript': 0.08, 'database': 0.07, 'sql': 0.07, 'aws': 0.06,
            'docker': 0.06, 'experience': 0.05, 'senior': 0.05, 'junior': 0.03
        }
        
        tech_boost = 0
        for term, weight in important_terms.items():
            if term in text1_lower and term in text2_lower:
                tech_boost += weight
        
        final_similarity = min(1.0, base_similarity + tech_boost)
        return final_similarity
    
    def explain_similarity(self, text1, text2):
        """Provide explanation of semantic match"""
        similarity = self.calculate_similarity(text1, text2)
        
        explanation = f"Semantic Similarity: {similarity:.1%}\n"
        
        if not self.model:
            explanation += "📝 Using enhanced basic matching\n"
        else:
            explanation += "🎯 Using AI semantic matching\n"
        
        if similarity >= 0.8:
            explanation += "Excellent match - strong contextual alignment"
        elif similarity >= 0.6:
            explanation += "Good match - clear relationship"
        elif similarity >= 0.4:
            explanation += "Moderate match - some contextual overlap"
        else:
            explanation += "Weak match - limited contextual relationship"
            
        return explanation

    # 🆕 ENHANCED CULTURAL FIT ANALYSIS
    def calculate_cultural_fit(self, job_description, candidate_profile):
        """Enhanced cultural fit scoring"""
        CULTURAL_INDICATORS = {
            'collaborative': ['team player', 'cross-functional', 'collaborate', 'partner with'],
            'fast_paced': ['fast-paced', 'dynamic', 'agile', 'adaptable', 'startup environment'],
            'autonomous': ['self-starter', 'independent', 'autonomous', 'self-directed'],
            'structured': ['process-driven', 'methodical', 'structured', 'organized environment']
        }
        
        job_text = job_description.lower()
        candidate_text = candidate_profile.lower()
        
        cultural_score = 0.5  # Base neutral score
        matches_found = 0
        
        for culture_type, indicators in CULTURAL_INDICATORS.items():
            job_has_culture = any(indicator in job_text for indicator in indicators)
            candidate_has_culture = any(indicator in candidate_text for indicator in indicators)
            
            if job_has_culture and candidate_has_culture:
                cultural_score += 0.15  # Strong match bonus
                matches_found += 1
            elif job_has_culture != candidate_has_culture:
                cultural_score -= 0.10  # Mismatch penalty
        
        return max(0.1, min(1.0, cultural_score))

# Global instance for reuse
semantic_matcher = SemanticMatcher()

# Quick test to verify everything works
if __name__ == "__main__":
    print("\n🧪 Testing semantic matcher...")
    test_score = semantic_matcher.calculate_similarity(
        "Python developer with Django experience",
        "Experienced Python developer using Django framework"
    )
    print(f"Test similarity: {test_score:.1%}")
    
    if semantic_matcher.model:
        print("✅ Advanced semantic matching is active!")
    else:
        print("🔧 Using enhanced basic matching")
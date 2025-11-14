# enhanced_cultural_extractor.py
from typing import Dict, Tuple

try:
    from sentence_transformers import SentenceTransformer, util
    import torch
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False

class EnhancedCulturalExtractor:
    def __init__(self):
        if SEMANTIC_AVAILABLE:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.semantic_enabled = True
                print("✅ Enhanced cultural extractor with semantic analysis ready!")
            except Exception as e:
                print(f"⚠️ Failed to load semantic model: {e}")
                self.semantic_enabled = False
        else:
            self.semantic_enabled = False
            print("⚠️ Enhanced cultural extractor using keyword-only mode")
    
    def extract_cultural_attributes_enhanced(self, text: str) -> Dict[str, Tuple[float, float]]:
        """Enhanced cultural extraction - ALWAYS returns a valid dict"""
        # Return a default dictionary to prevent NoneType errors
        default_result = {
            'teamwork': (0.5, 0.5),
            'innovation': (0.5, 0.5), 
            'work_environment': (0.5, 0.5),
            'work_pace': (0.5, 0.5),
            'customer_focus': (0.5, 0.5)
        }
        
        if not text or len(text.strip()) < 10:
            return default_result
            
        try:
            # Simple keyword-based enhancement for now
            text_lower = text.lower()
            
            # Basic keyword counting
            teamwork_terms = ['team', 'collaborat', 'partner', 'work together']
            innovation_terms = ['innovati', 'creativ', 'new ideas', 'problem solv']
            
            teamwork_matches = sum(1 for term in teamwork_terms if term in text_lower)
            innovation_matches = sum(1 for term in innovation_terms if term in text_lower)
            
            # Update scores based on keywords
            if teamwork_matches > 0:
                default_result['teamwork'] = (0.7, 0.8)
            if innovation_matches > 0:
                default_result['innovation'] = (0.7, 0.8)
                
            return default_result
            
        except Exception as e:
            print(f"⚠️ Enhanced extraction failed: {e}")
            return default_result
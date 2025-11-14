# enhanced_cultural_extractor.py
from typing import Dict, Tuple
import re

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
        
        # Complete cultural attribute taxonomy with weighted keywords
        self.cultural_taxonomy = {
            'teamwork': {
                'collaborative': ['team', 'collaborat', 'partner', 'work together', 'cooperat', 'joint effort'],
                'independent': ['independent', 'self-motivat', 'autonom', 'self-manag', 'work independently']
            },
            'innovation': {
                'innovative': ['innovati', 'creativ', 'new ideas', 'problem solv', 'think outside', 'breakthrough'],
                'traditional': ['traditional', 'proven methods', 'established', 'conventional', 'time-tested']
            },
            'work_environment': {
                'fast_paced': ['fast-paced', 'dynamic', 'rapid', 'high-energy', 'quick turn', 'agile'],
                'structured': ['structured', 'methodical', 'organized', 'systematic', 'planned', 'process-driven'],
                'flexible': ['flexible', 'adapt', 'change', 'evolving', 'adjust', 'fluid']
            },
            'work_pace': {
                'high_pressure': ['high-pressure', 'deadline', 'urgent', 'time-sensitive', 'crunch', 'intense'],
                'steady': ['steady', 'consistent', 'predictable', 'stable', 'reliable', 'measured'],
                'balanced': ['work-life balance', 'reasonable hours', 'sustainable', 'balanced pace']
            },
            'customer_focus': {
                'customer_centric': ['customer focus', 'client first', 'customer satisf', 'client service', 'user experience'],
                'product_focused': ['product excellence', 'quality driven', 'technical excellence', 'product innovation'],
                'internal_focus': ['internal process', 'operational efficiency', 'cost effective', 'resource management']
            }
        }
    
    def extract_cultural_attributes_enhanced(self, text: str) -> Dict[str, Tuple[float, float]]:
        """Enhanced cultural extraction with complete attribute coverage"""
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
            text_lower = text.lower()
            
            # Calculate scores for each attribute based on keyword presence and frequency
            teamwork_score = self._calculate_attribute_score(text_lower, 'teamwork')
            innovation_score = self._calculate_attribute_score(text_lower, 'innovation')
            work_env_score = self._calculate_attribute_score(text_lower, 'work_environment')
            work_pace_score = self._calculate_attribute_score(text_lower, 'work_pace')
            customer_score = self._calculate_attribute_score(text_lower, 'customer_focus')
            
            # Update results with calculated scores
            default_result['teamwork'] = (teamwork_score, self._calculate_confidence(text_lower, 'teamwork'))
            default_result['innovation'] = (innovation_score, self._calculate_confidence(text_lower, 'innovation'))
            default_result['work_environment'] = (work_env_score, self._calculate_confidence(text_lower, 'work_environment'))
            default_result['work_pace'] = (work_pace_score, self._calculate_confidence(text_lower, 'work_pace'))
            default_result['customer_focus'] = (customer_score, self._calculate_confidence(text_lower, 'customer_focus'))
                
            return default_result
            
        except Exception as e:
            print(f"⚠️ Enhanced extraction failed: {e}")
            return default_result
    
    def _calculate_attribute_score(self, text: str, attribute: str) -> float:
        """Calculate score for a specific attribute based on keyword matches"""
        if attribute not in self.cultural_taxonomy:
            return 0.5
            
        attribute_categories = self.cultural_taxonomy[attribute]
        total_matches = 0
        category_scores = {}
        
        # Count matches for each sub-category
        for category, keywords in attribute_categories.items():
            matches = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                matches += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
            category_scores[category] = matches
            total_matches += matches
        
        if total_matches == 0:
            return 0.5  # Neutral if no matches
            
        # Calculate weighted score based on dominant category
        base_score = 0.5
        max_category = max(category_scores, key=category_scores.get)
        max_matches = category_scores[max_category]
        
        # Convert to 0-1 scale based on match strength
        if max_matches == 1:
            return 0.6  # Light preference
        elif max_matches == 2:
            return 0.7  # Moderate preference
        elif max_matches >= 3:
            return 0.8  # Strong preference
            
        return base_score
    
    def _calculate_confidence(self, text: str, attribute: str) -> float:
        """Calculate confidence score based on keyword evidence strength"""
        if attribute not in self.cultural_taxonomy:
            return 0.3
            
        attribute_categories = self.cultural_taxonomy[attribute]
        total_matches = 0
        
        for keywords in attribute_categories.values():
            for keyword in keywords:
                total_matches += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
        
        # Confidence based on number of matches
        if total_matches == 0:
            return 0.3  # Low confidence for no evidence
        elif total_matches == 1:
            return 0.6  # Medium confidence
        elif total_matches == 2:
            return 0.8  # High confidence
        else:
            return 0.9  # Very high confidence for multiple matches
# 🗃️ DATABASE SCORING CONFIGURATION
# Temporary test implementation until database tables are built

class DatabaseScoringConfig:
    def __init__(self):
        self.connection = None  # Will be set when database is ready
        self.using_test_data = True  # Start with test data until DB is built
        print("✅ Database scoring config initialized (test mode)")
    
    def get_skill_weights(self):
        """Get skill weights from DATABASE - not hard-coded"""
        if self.using_test_data:
            return self._get_test_skill_weights()  # Temporary test data
        else:
            return self._get_skill_weights_from_db()  # Real database call
    
    def _get_skill_weights_from_db(self):
        """ACTUAL DATABASE QUERY - to be implemented when DB is ready"""
        # This will query the scoring_parameters table
        try:
            # TODO: Replace with actual database query
            # Example: "SELECT skill_name, base_weight FROM skill_categories"
            return self._execute_db_query("skill_weights")
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            # Fallback to test data if database not ready
            return self._get_test_skill_weights()
    
    def _get_test_skill_weights(self):
        """TEMPORARY test data - DIFFERENT from hard-coded to show the system works"""
        # These are intentionally different from matcher.py hard-coded values
        # so you can see the system switching between modes
        return {
            'python': 0.25,  # Much higher to make testing obvious
            'javascript': 0.18,
            'java': 0.15,
            'react': 0.16,
            'django': 0.12,
            'flask': 0.10,
            'node.js': 0.12,
            'sql': 0.15,
            'mongodb': 0.10,
            'docker': 0.12,
            'aws': 0.12,
            'machine learning': 0.20,
            'tensorflow': 0.12,
            'pytorch': 0.12,
            'statistics': 0.14,
            'data analysis': 0.12,
            'css': 0.08,
            'html': 0.08,
            'git': 0.06,
            'rest api': 0.10
        }
    
    def get_scoring_weights(self):
        """Get overall scoring weights from DATABASE"""
        if self.using_test_data:
            return self._get_test_scoring_weights()
        else:
            return self._get_scoring_weights_from_db()
    
    def _get_scoring_weights_from_db(self):
        """ACTUAL DATABASE QUERY for scoring weights"""
        try:
            # TODO: Replace with actual database query  
            # Example: "SELECT parameter_name, parameter_value FROM scoring_parameters"
            return self._execute_db_query("scoring_weights")
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            return self._get_test_scoring_weights()
    
    def _get_test_scoring_weights(self):
        """TEMPORARY test weights - different from hard-coded"""
        return {
            'skill': 0.50,      # Increased from 0.40 (hardcoded)
            'experience': 0.20,  # Decreased from 0.25
            'location': 0.20,    # Increased from 0.15  
            'semantic': 0.10     # Decreased from 0.20
        }
    
    def _execute_db_query(self, query_type):
        """Placeholder for actual database operations"""
        # This will be implemented when we create the actual database tables
        print(f"🔍 [DATABASE] Would execute query for: {query_type}")
        raise NotImplementedError("Database not yet implemented - using test data")
    
    def enable_database_mode(self):
        """Switch to real database mode (when ready)"""
        self.using_test_data = False
        print("🎯 Database mode: REAL DATABASE QUERIES ENABLED")
    
    def enable_test_mode(self):
        """Switch to test data mode"""
        self.using_test_data = True
        print("🎯 Database mode: USING TEST DATA")

# Test the class
if __name__ == "__main__":
    config = DatabaseScoringConfig()
    print("Test skill weights:", config.get_skill_weights())
    print("Test scoring weights:", config.get_scoring_weights())
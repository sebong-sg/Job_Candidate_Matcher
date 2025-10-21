# 🗃️ DATABASE SCORING CONFIGURATION
# Temporary test implementation until database tables are built
# KEEP EXISTING CLASS - ENHANCE IT for database tables

# def initialize_database():
#    """Initialize the SQLite database with all tables"""
#    from database import Database
#    db = Database()  # This will create the database file and tables
#    print("✅ Database initialized with all tables")

# Call this function before using any database operations
# initialize_database()

class DatabaseScoringConfig:
    def __init__(self):
        self.connection = None  # Will be set when database is ready
        self.using_test_data = True  # Start with test data until DB is built
        self.scoring_db = ScoringDB()  # ADD THIS LINE
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
        # These are intentionally different from matcher.py hard-coded valuesF
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
        """ACTUAL DATABASE QUERY for scoring weights - NOW IMPLEMENTED"""
        try:
            print(f"🔍 DEBUG: using_test_data = {self.using_test_data}") # temporary Debug code 
            # Use the first user's default profile
            users = self.scoring_db.get_all_users()
            print(f"🔍 DEBUG: Found {len(users)} users") # temporary Debug code 
            if users:
                user_id = users[0][0]  # First user
                profiles = self.scoring_db.get_user_profiles(user_id)
                if profiles:
                    profile_id = profiles[0][0]  # Default profile
                    params = self.scoring_db.get_scoring_parameters(profile_id)
                    # Return ACTUAL values from database
                    return params['criteria']  # Returns {'skills': 0.4, 'experience': 0.3, ...}
        
            return self._get_test_scoring_weights()  # Fallback
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            return self._get_test_scoring_weights()
    
############ Original working code for def _get_scoring_weights_from_db()
#    def _get_scoring_weights_from_db(self):
#        """ACTUAL DATABASE QUERY for scoring weights"""
#        try:
#            # TODO: Replace with actual database query  
#            # Example: "SELECT parameter_name, parameter_value FROM scoring_parameters"
#            return self._execute_db_query("scoring_weights")
#        except Exception as e:
#            print(f"❌ Database query failed: {e}")
#            return self._get_test_scoring_weights()
##############

    def _get_test_scoring_weights(self):
        """TEMPORARY test weights - different from hard-coded"""
        return {
            'skills': 0.50,      # Increased from 0.40 (hardcoded)
            'experience': 0.20,  # Decreased from 0.25
            'location': 0.20,    # Increased from 0.15  
            'semantic': 0.10,     # Decreased from 0.20
            'cultural_fit': 0.10, 
            'growth_potential': 0.05
        }


    def _execute_db_query(self, query_type):
        """ACTUAL DATABASE OPERATIONS - NOW IMPLEMENTED"""
        try:
            if query_type == "scoring_weights":
                return self._get_scoring_weights_from_db()
            elif query_type == "skill_weights":
#                return self._get_skill_weights_from_db()
                # Skill weights not implemented in SQLite yet
                raise NotImplementedError("Skill weights table not implemented in SQLite yet")
            else:
                raise ValueError(f"Unknown query type: {query_type}")
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            raise

 ############ Original working def _execute_db_query()  
 #   def _execute_db_query(self, query_type):
 #       """Placeholder for actual database operations"""
 #       # This will be implemented when we create the actual database tables
 #       print(f"🔍 [DATABASE] Would execute query for: {query_type}")
 #       raise NotImplementedError("Database not yet implemented - using test data")
############
    
    def enable_database_mode(self):
        """Switch to real database mode (when ready)"""
        self.using_test_data = False
        print("🎯 Database mode: REAL DATABASE QUERIES ENABLED")
    
    def enable_test_mode(self):
        """Switch to test data mode"""
        self.using_test_data = True
        print("🎯 Database mode: USING TEST DATA")


class ScoringDB:
    def __init__(self, db_path='job_matcher.db'):
        from database import Database
        self.db = Database(db_path)
        self._create_default_data()
    
    def _create_default_data(self):
        """Create 5 test users with default profiles using hardcoded values"""
        # Check if data already exists
        if self.db.conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
            return
            
        # Create test company
        cursor = self.db.conn.execute(
            "INSERT INTO companies (name) VALUES (?)",
            ("Test Corporation",)
        )
        # company_id = self.db.conn.lastrowid # error replace with below
        cursor = self.db.conn.execute("INSERT INTO companies (name) VALUES (?)", ("Test Corporation",))
        company_id = cursor.lastrowid

        # Create 5 test users
        test_users = [
            (company_id, "recruiter_john", "john@test.com", "Recruiter"),
            (company_id, "hm_sarah", "sarah@test.com", "Hiring Manager"),
            (company_id, "ta_mike", "mike@test.com", "TA Manager"),
            (company_id, "recruiter_anna", "anna@test.com", "Recruiter"),
            (company_id, "hm_david", "david@test.com", "Hiring Manager")
        ]
        
        created_user_ids = []  # Use a different variable name
        for user_data in test_users:  # Use different variable name
            cursor = self.db.conn.execute(
                "INSERT INTO users (company_id, username, email, role) VALUES (?, ?, ?, ?)",
                user_data
            )
            created_user_ids.append(cursor.lastrowid)
        
        # Create default profile for each user with hardcoded values
              
        for user_id in created_user_ids:
            self._create_user_default_profile(user_id)

        self.db.conn.commit()
        print("✅ Created 5 test users with default scoring profiles")
    
    def _create_user_default_profile(self, user_id):
        """Create default profile for a user"""
        cursor = self.db.conn.execute(  # ← Define cursor first
#        self.db.conn.execute(
            "INSERT INTO scoring_profiles (user_id, profile_name, is_default) VALUES (?, ?, ?)",
            (user_id, "Default Profile", True)
        )
        profile_id = cursor.lastrowid
        
        # Add scoring criteria (current hardcoded weights)
        criteria = [
            (profile_id, "skills", 0.4),
            (profile_id, "experience", 0.3),
            (profile_id, "education", 0.15),
            (profile_id, "location", 0.1),
            (profile_id, "industry", 0.05)
        ]
        self.db.conn.executemany(
            "INSERT INTO scoring_criteria (profile_id, name, weight) VALUES (?, ?, ?)",
            criteria
        )
        
        # Add thresholds
        thresholds = [
            (profile_id, "minimum_score", 60),
            (profile_id, "senior_exp", 5),
            (profile_id, "mid_exp", 3),
            (profile_id, "junior_exp", 1)
        ]
        self.db.conn.executemany(
            "INSERT INTO scoring_thresholds (profile_id, name, value) VALUES (?, ?, ?)",
            thresholds
        )
        
        # Add experience mappings
        exp_mappings = [
            (profile_id, "experience", "entry", 1),
            (profile_id, "experience", "mid", 2),
            (profile_id, "experience", "senior", 3)
        ]
        self.db.conn.executemany(
            "INSERT INTO scoring_mappings (profile_id, type, key, value) VALUES (?, ?, ?, ?)",
            exp_mappings
        )
        
        # Add education mappings
        edu_mappings = [
            (profile_id, "education", "high_school", 1),
            (profile_id, "education", "bachelor", 2),
            (profile_id, "education", "master", 3),
            (profile_id, "education", "phd", 4)
        ]
        self.db.conn.executemany(
            "INSERT INTO scoring_mappings (profile_id, type, key, value) VALUES (?, ?, ?, ?)",
            edu_mappings
        )
        
        # Add job level keywords
        keywords = [
            (profile_id, "senior", '["senior", "lead", "principal"]'),
            (profile_id, "junior", '["junior", "entry"]')
        ]
        self.db.conn.executemany(
            "INSERT INTO job_level_keywords (profile_id, level, keywords) VALUES (?, ?, ?)",
            keywords
        )
    
    def get_all_users(self):
        """Get all users for UI dropdown"""
        return self.db.conn.execute(
            "SELECT id, username, role FROM users ORDER BY username"
        ).fetchall()
    
    def get_user_profiles(self, user_id):
        """Get all profiles for a user"""
        return self.db.conn.execute(
            "SELECT id, profile_name, is_default FROM scoring_profiles WHERE user_id = ? ORDER BY is_default DESC, profile_name",
            (user_id,)
        ).fetchall()
    
    def get_scoring_parameters(self, profile_id):
        """Get all scoring parameters for a profile"""
        criteria = self.db.conn.execute(
            "SELECT name, weight FROM scoring_criteria WHERE profile_id = ? AND is_active = TRUE",
            (profile_id,)
        ).fetchall()
        
        thresholds = self.db.conn.execute(
            "SELECT name, value FROM scoring_thresholds WHERE profile_id = ?",
            (profile_id,)
        ).fetchall()
        
        mappings = self.db.conn.execute(
            "SELECT type, key, value FROM scoring_mappings WHERE profile_id = ?",
            (profile_id,)
        ).fetchall()
        
        keywords = self.db.conn.execute(
            "SELECT level, keywords FROM job_level_keywords WHERE profile_id = ?",
            (profile_id,)
        ).fetchall()
        
        return {
            'criteria': dict(criteria),
            'thresholds': dict(thresholds),
            'mappings': mappings,
            'keywords': dict(keywords)
        }

# Test the class
if __name__ == "__main__":
    config = DatabaseScoringConfig()
    print("Test skill weights:", config.get_skill_weights())
    print("Test scoring weights:", config.get_scoring_weights())    

# Test the class
if __name__ == "__main__":
    config = DatabaseScoringConfig()
    print("Test skill weights:", config.get_skill_weights())
    print("Test scoring weights:", config.get_scoring_weights())
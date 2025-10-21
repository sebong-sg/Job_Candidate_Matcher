# test_database_setup.py
import sys
import os
# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database_scoring import DatabaseScoringConfig

def test_database_setup():
    print("🧪 Testing Database Setup...")
    
    # Initialize scoring config
    config = DatabaseScoringConfig()
    
    # Test 1: Check if users exist
    users = config.scoring_db.get_all_users()
    print(f"✅ Users in database: {len(users)}")
    for user in users:
        print(f"   - {user[1]} ({user[2]})")
    
    # Test 2: Check if profiles exist for first user
    if users:
        user_id = users[0][0]
        profiles = config.scoring_db.get_user_profiles(user_id)
        print(f"✅ Profiles for user {user_id}: {len(profiles)}")
        for profile in profiles:
            print(f"   - {profile[1]} (default: {profile[2]})")
    
    # Test 3: Check scoring parameters for first profile
    if users and profiles:
        profile_id = profiles[0][0]
        params = config.scoring_db.get_scoring_parameters(profile_id)
        print("✅ Scoring parameters:")
        print(f"   Criteria: {params['criteria']}")
        print(f"   Thresholds: {params['thresholds']}")
        print(f"   Mappings: {params['mappings']}")
        print(f"   Keywords: {params['keywords']}")

    # NEW: Database State Check
    print("\n🔍 Database State Check:")
    users = config.scoring_db.db.conn.execute("SELECT id, username FROM users").fetchall()
    print(f"Users: {users}")

    profiles = config.scoring_db.db.conn.execute("SELECT id, user_id FROM scoring_profiles").fetchall()
    print(f"Profiles: {profiles}")

    # Check if there are any database errors
    tables = config.scoring_db.db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"All tables: {[t[0] for t in tables]}")
    


    # Test 4: Test database mode
    print("\n🧪 Testing Database Mode Switch...")
    config.enable_database_mode()
    scoring_weights = config.get_scoring_weights()
    print(f"✅ Database mode weights: {scoring_weights}")

if __name__ == "__main__":
    test_database_setup()
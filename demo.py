# 🎮 DEMO FILE - Now with Database!
# Easy way to run and see semantic matching results

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from matcher import main

print("🎪 WELCOME TO JOB MATCHER DEMO!")
print("Now with SEMANTIC DATABASE matching!")
print("=" * 60)
print("This will:")
print("1. 📁 Load jobs and candidates from database files")
print("2. 🤖 Use AI to find semantic matches")  
print("3. 📊 Show you the best candidates for each job")
print("=" * 60)

if __name__ == "__main__":
    main()
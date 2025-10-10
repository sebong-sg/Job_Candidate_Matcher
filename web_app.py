# 🎮 ONE-CLICK WEB APP LAUNCHER
# Run this to start the beautiful web interface!

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from web_interface import main

print("🌐 JOB MATCHER WEB APP")
print("======================")
print("Starting web interface...")
print("This will open an interactive menu system!")
print("No browser needed - everything runs in terminal!")
print("=" * 50)

if __name__ == "__main__":
    main()
# 📊 ONE-CLICK ANALYTICS LAUNCHER

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analytics import main

print("📈 JOB MATCHER ANALYTICS")
print("========================")
print("Generating comprehensive report...")
print("This will show you insights about your data!")
print("=" * 50)

if __name__ == "__main__":
    main()
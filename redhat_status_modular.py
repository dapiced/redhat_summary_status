#!/usr/bin/env python3
"""
Red Hat Status Checker - Modular Version Launcher

This script provides an easy way to run the modular version
of the Red Hat Status Checker with the same interface as
the original monolithic script.

Usage:
    ./redhat_status_modular.py [options]
    
This maintains full backward compatibility while providing
the benefits of the new modular architecture.
"""

import sys
import os
from pathlib import Path

# Add the redhat_status directory to Python path
script_dir = Path(__file__).parent
redhat_status_dir = script_dir / "redhat_status"
sys.path.insert(0, str(script_dir))

# Import and run the main application
if __name__ == "__main__":
    try:
        from redhat_status.main import main
        main()
    except ImportError as e:
        print(f"❌ Error importing modular components: {e}")
        print("Make sure all modular components are properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
Startup script for Voice Height Guesser
"""

import os
import sys
import subprocess

def main():
    # Get the directory of this script
    root_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(root_dir, 'height_guesser')
    
    # Check if the app directory exists
    if not os.path.exists(app_dir):
        print(f"Error: Application directory '{app_dir}' not found.")
        return 1
    
    # Change to the app directory
    os.chdir(app_dir)
    
    # Run the application
    try:
        # Execute run.py script in the app directory
        subprocess.check_call([sys.executable, 'run.py'])
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running the application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
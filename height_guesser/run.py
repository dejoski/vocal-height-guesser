#!/usr/bin/env python3

import os
import sys
import subprocess

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    """Main function to run the application"""
    # Check if requirements are installed
    try:
        import flask
        import librosa
        import numpy
        import sklearn
    except ImportError:
        print("Some required packages are missing.")
        choice = input("Do you want to install them now? (y/n): ")
        if choice.lower() == 'y':
            install_requirements()
        else:
            print("Cannot run the application without required packages.")
            sys.exit(1)
    
    # Import the app after dependencies are confirmed
    from app import app
    
    # Run the app
    print("Starting Voice Height Guesser...")
    print("Open your browser and go to http://127.0.0.1:5000")
    app.run(debug=True)

if __name__ == "__main__":
    # Change to the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    main() 
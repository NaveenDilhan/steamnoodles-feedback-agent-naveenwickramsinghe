#!/usr/bin/env python3
"""
Setup script for SteamNoodles Multi-Agent Framework
Automates the initial setup process
"""

import os
import sys
import subprocess
import platform

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        'agents',
        'config', 
        'utils',
        'data',
        'outputs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Create __init__.py files for Python packages
        if directory in ['agents', 'config', 'utils']:
            init_file = os.path.join(directory, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write(f'"""{directory.title()} package"""\n')
    
    print("✓ Directory structure created")

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    except FileNotFoundError:
        print("✗ requirements.txt not found")
        return False
    
    return True

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} may not be compatible")
        print("Recommended: Python 3.8 or higher")
        return False

def create_env_template():
    """Create .env template file"""
    env_template = """# SteamNoodles AI Configuration
# Copy this file to .env and add your actual API key

OPENAI_API_KEY=your-openai-api-key-here

# Optional: Uncomment and modify these settings
# DEFAULT_TEMPERATURE=0.7
# MAX_TOKENS=200
# AGENT_VERBOSE=True
"""
    
    env_file = '.env.template'
    with open(env_file, 'w') as f:
        f.write(env_template)
    
    print(f"✓ Environment template created: {env_file}")
    print("  Please copy this to .env and add your OpenAI API key")

def run_initial_test():
    """Run a basic test to ensure setup is working"""
    print("\nRunning initial test...")
    
    try:
        # Test imports
        import langchain
        import openai
        import pandas as pd
        import matplotlib.pyplot as plt
        print("✓ All required packages can be imported")
        
        # Test data generation
        from utils.data_generator import generate_sample_data
        if not os.path.exists('data/restaurant_reviews.csv'):
            print("Generating sample data...")
            generate_sample_data(50, 7)  # Small dataset for testing
        
        print("✓ Initial test completed successfully")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("SteamNoodles Multi-Agent Framework Setup")
    print("=" * 45)
    
    # Check Python version
    if not check_python_version():
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create directory structure
    create_directory_structure()
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed due to dependency installation issues")
        sys.exit(1)
    
    # Create environment template
    create_env_template()
    
    # Run initial test
    test_passed = run_initial_test()
    
    print("\n" + "=" * 45)
    if test_passed:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Copy .env.template to .env")
        print("2. Add your OpenAI API key to .env")
        print("3. Run: python main.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("Please check the error messages above and resolve any issues")
    
    print(f"\nPlatform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")

if __name__ == "__main__":
    main()
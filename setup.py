"""
Setup script to initialize the project
Creates necessary directories and checks dependencies
"""

import os
import sys


def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        "agents",
        "tools",
        "data",
        "data/travel_knowledge",
        "data/chroma_db",
    ]

    print("📁 Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✓ {directory}/")

    # Create __init__.py files for Python packages
    init_files = [
        "agents/__init__.py",
        "tools/__init__.py",
    ]

    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('"""Package initialization"""\n')

    print("✅ Directory structure created\n")


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("⚠️  .env file not found!")
        print("📝 Creating .env file from template...")

        if os.path.exists(".env.example"):
            with open(".env.example", 'r') as f:
                content = f.read()
            with open(".env", 'w') as f:
                f.write(content)
            print("✅ .env file created")
            print("⚠️  Please edit .env and add your OPENAI_API_KEY\n")
        else:
            print("❌ .env.example not found")
            print("Please create a .env file with OPENAI_API_KEY=your_key_here\n")
    else:
        print("✅ .env file exists\n")


def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")

    required_packages = [
        "crewai",
        "langchain",
        "langchain_openai",
        "chromadb",
        "openai",
        "dotenv",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt\n")
        return False
    else:
        print("✅ All dependencies installed\n")
        return True


def main():
    print("=" * 60)
    print("🚀 Multi-Agent RAG Travel Planner - Setup")
    print("=" * 60)
    print()

    create_directory_structure()
    check_env_file()
    deps_ok = check_dependencies()

    print("=" * 60)
    if deps_ok:
        print("✅ Setup complete! You're ready to go.")
        print()
        print("Next steps:")
        print("1. Add your OPENAI_API_KEY to the .env file")
        print("2. Run: python main.py")
    else:
        print("⚠️  Setup incomplete. Please install missing dependencies.")
        print("Run: pip install -r requirements.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()

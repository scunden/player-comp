#!/bin/bash

# Define the root directory
root_dir="compare_players_app"

# Create the directory structure
mkdir -p "$root_dir"/app/pages
mkdir -p "$root_dir"/data/raw
mkdir -p "$root_dir"/data/processed
mkdir -p "$root_dir"/scrapers
mkdir -p "$root_dir"/notebooks

mkdir -p "$root_dir"/tests

# Create __init__.py files for Python modules
touch "$root_dir"/app/__init__.py
touch "$root_dir"/app/pages/__init__.py
touch "$root_dir"/scrapers/__init__.py
touch "$root_dir"/tests/__init__.py

# Create main and utility scripts
touch "$root_dir"/app/main.py
touch "$root_dir"/app/utils.py

# Create page scripts
touch "$root_dir"/app/pages/home.py
touch "$root_dir"/app/pages/analysis.py
touch "$root_dir"/app/pages/about.py

# Create scraper scripts
touch "$root_dir"/scrapers/scraper1.py
touch "$root_dir"/scrapers/scraper2.py

# Create test scripts
touch "$root_dir"/tests/test_app.py
touch "$root_dir"/tests/test_scrapers.py

touch "$root_dir"/notebooks/sandbox.ipynb


# Create requirements and README files
touch "$root_dir"/requirements.txt
touch "$root_dir"/README.md

echo "Project structure created successfully in $root_dir/"

# chmod +x create_structure.sh
# ./create_structure.sh
#!/usr/bin/env python3
import json
import re
from datetime import datetime

def get_grade_color(grade):
    """Return color code based on grade"""
    colors = {
        "A+": "FFD700",  # Gold
        "A": "FFA500",   # Orange
        "B+": "90EE90",  # Light Green
        "B": "87CEEB",   # Sky Blue
        "C+": "FFB6C1",  # Light Pink
        "C": "D3D3D3",   # Light Gray
        "D": "FF6347",   # Tomato Red
    }
    return colors.get(grade, "CCCCCC")

def create_grade_badge(grade, score):
    """Create a badge URL"""
    color = get_grade_color(grade)
    label = f"Contribution%20Grade"
    message = f"{grade}%20%7C%20{score}%25"
    
    badge_url = f"https://img.shields.io/badge/{label}-{message}-{color}?style=for-the-badge&logo=github&logoColor=white"
    return badge_url

def update_readme(grade, score):
    """Update README.md with new grade badge"""
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: README.md not found")
        return False
    
    badge_url = create_grade_badge(grade, score)
    new_badge = f'  <img src="{badge_url}" alt="Contribution Grade: {grade}"/>'
    
    # Pattern to match existing grade badge
    pattern = r'<img src="https://img\.shields\.io/badge/Contribution%20Grade[^"]*" alt="Contribution Grade:[^"]*"/>'
    
    if re.search(pattern, content):
        # Replace existing badge
        content = re.sub(pattern, new_badge.strip(), content)
        print("✅ Updated existing grade badge")
    else:
        print("⚠️  No existing badge found, adding new one")
    
    # Write updated content
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ README.md updated with grade {grade} ({score}%)")
        return True
    except Exception as e:
        print(f"Error writing README.md: {e}")
        return False

def main():
    try:
        with open(".github/grade_data.json", "r") as f:
            grade_data = json.load(f)
    except FileNotFoundError:
        print("Error: grade_data.json not found")
        return
    
    grade = grade_data.get("grade")
    score = grade_data.get("score")
    
    if grade and score is not None:
        update_readme(grade, score)
    else:
        print("Error: Invalid grade data")

if __name__ == "__main__":
    main()

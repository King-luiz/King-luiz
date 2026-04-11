#!/usr/bin/env python3
import json
import re
from datetime import datetime

def get_grade_color(grade):
    """Return color code based on grade"""
    colors = {
        "A+": "00FFAA",  # Bright Green
        "A": "FFA500",   # Orange
        "B+": "90EE90",  # Light Green
        "B": "87CEEB",   # Sky Blue
        "C+": "FFB6C1",  # Light Pink
        "C": "D3D3D3",   # Light Gray
        "D": "FF6347",   # Tomato Red
    }
    return colors.get(grade, "CCCCCC")

def create_circular_svg(grade, color):
    """Create circular SVG badge"""
    svg = f'''<svg width="180" height="180" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">
      <!-- Background circle -->
      <circle cx="90" cy="90" r="85" fill="#1a1a2e" stroke="#{color}" stroke-width="3"/>
      <!-- Grade text -->
      <text x="90" y="115" font-size="72" font-weight="bold" text-anchor="middle" fill="#{color}" font-family="Arial, sans-serif">{grade}</text>
    </svg>'''
    return svg

def create_grade_badge(grade, score):
    """Create a badge URL"""
    color = get_grade_color(grade)
    label = f"Contribution%20Grade"
    message = f"{grade}%20%7C%20High" if score >= 70 else f"{grade}%20%7C%20Medium" if score >= 50 else f"{grade}%20%7C%20Low"
    
    badge_url = f"https://img.shields.io/badge/{label}-{message}-{color}?style=for-the-badge&logo=github&logoColor=black"
    return badge_url

def update_readme(grade, score):
    """Update README.md with new grade badge"""
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: README.md not found")
        return False
    
    color = get_grade_color(grade)
    svg_badge = create_circular_svg(grade, color)
    badge_url = create_grade_badge(grade, score)
    
    # Pattern to match existing SVG circle
    svg_pattern = r'<svg width="180" height="180"[^>]*>.*?</svg>'
    
    if re.search(svg_pattern, content, re.DOTALL):
        content = re.sub(svg_pattern, svg_badge, content, flags=re.DOTALL)
        print("✅ Updated circular SVG badge")
    
    # Pattern to match existing text badge
    badge_pattern = r'<img src="https://img\.shields\.io/badge/Contribution%20Grade[^"]*" alt="Contribution Grade:[^"]*"/>'
    
    if re.search(badge_pattern, content):
        new_badge = f'<img src="{badge_url}" alt="Contribution Grade: {grade}"/>'
        content = re.sub(badge_pattern, new_badge, content)
        print("✅ Updated text badge")
    
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

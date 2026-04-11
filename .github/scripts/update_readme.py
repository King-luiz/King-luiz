import json
import re
from datetime import datetime

def get_grade_color(grade):
    colors = {
        "A+": "FFD700",
        "A": "FFA500",
        "B+": "90EE90",
        "B": "87CEEB",
        "C+": "FFB6C1",
        "C": "D3D3D3",
        "D": "FF6347",
    }
    return colors.get(grade, "CCCCCC")

def create_grade_badge(grade, score):
    color = get_grade_color(grade)
    label = f"Contribution%20Grade"
    message = f"{grade}%20%7C%20{score}%25"
    badge_url = f"https://img.shields.io/badge/{label}-{message}-{color}?style=for-the-badge&logo=github&logoColor=white"
    return badge_url

def update_readme(grade, score):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    badge_url = create_grade_badge(grade, score)
    new_badge = f'  <img src="{badge_url}" alt="Contribution Grade: {grade}"/>'
    
    pattern = r'<img src="https://img\.shields\.io/badge/Contribution%20Grade.*?" alt="Contribution Grade:.*?"/>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, new_badge.strip(), content)
    else:
        if "## 🎖️ Contribution Grade & Achievements" in content:
            section_pattern = r"(## 🎖️ Contribution Grade & Achievements\s*<div align=\"center\">\s*)"
            insertion = r'\1' + new_badge + '\n  '
            content = re.sub(section_pattern, insertion, content)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    try:
        with open(".github/grade_data.json", "r") as f:
            grade_data = json.load(f)
    except FileNotFoundError:
        return
    
    grade = grade_data.get("grade")
    score = grade_data.get("score")
    
    if grade and score is not None:
        update_readme(grade, score)

if __name__ == "__main__":
    main()

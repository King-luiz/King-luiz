#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

def get_user_stats(username, token):
    """Fetch GitHub user statistics"""
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    query = """
    query($userName:String!) {
      user(login: $userName) {
        repositories(first: 100) {
          totalCount
        }
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
        }
        followers {
          totalCount
        }
        pullRequests(first: 100) {
          totalCount
        }
        issues(first: 100) {
          totalCount
        }
      }
    }
    """
    
    variables = {"userName": username}
    
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]["user"]:
            return data["data"]["user"]
    
    print(f"Error fetching user data: {response.status_code}")
    return None

def calculate_grade(stats):
    """Calculate grade based on metrics"""
    
    if not stats:
        return "D", 0
    
    contrib = stats.get("contributionsCollection", {})
    
    commits = contrib.get("totalCommitContributions", 0)
    pull_requests = stats.get("pullRequests", {}).get("totalCount", 0)
    issues = stats.get("issues", {}).get("totalCount", 0)
    repositories = stats.get("repositories", {}).get("totalCount", 0)
    followers = stats.get("followers", {}).get("totalCount", 0)
    
    # Normalize metrics (scale to 0-100)
    commit_score = min(100, (commits / 500) * 100)
    pr_score = min(100, (pull_requests / 100) * 100)
    issue_score = min(100, (issues / 50) * 100)
    repo_score = min(100, (repositories / 30) * 100)
    follower_score = min(100, (followers / 100) * 100)
    
    # Weighted calculation
    total_score = (
        (commit_score * 0.40) +
        (pr_score * 0.20) +
        (issue_score * 0.15) +
        (repo_score * 0.15) +
        (follower_score * 0.10)
    )
    
    # Determine grade
    if total_score >= 90:
        grade = "A+"
    elif total_score >= 85:
        grade = "A"
    elif total_score >= 80:
        grade = "B+"
    elif total_score >= 70:
        grade = "B"
    elif total_score >= 60:
        grade = "C+"
    elif total_score >= 50:
        grade = "C"
    else:
        grade = "D"
    
    return grade, round(total_score, 2)

def main():
    username = os.getenv("GITHUB_USER", "King-luiz")
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("Error: GITHUB_TOKEN not found")
        return
    
    print(f"Calculating grade for @{username}...")
    
    stats = get_user_stats(username, token)
    
    if stats:
        grade, score = calculate_grade(stats)
        
        # Save to file
        grade_data = {
            "username": username,
            "grade": grade,
            "score": score,
            "timestamp": datetime.now().isoformat(),
        }
        
        with open(".github/grade_data.json", "w") as f:
            json.dump(grade_data, f, indent=2)
        
        print(f"✅ Grade: {grade} ({score}%)")
    else:
        print("❌ Failed to fetch stats")

if __name__ == "__main__":
    main()

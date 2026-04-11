def calculate_grade(stats):
    """Calculate grade based on metrics - Beginner Friendly"""
    
    if not stats:
        return "D", 0
    
    contrib = stats.get("contributionsCollection", {})
    
    commits = contrib.get("totalCommitContributions", 0)
    pull_requests = stats.get("pullRequests", {}).get("totalCount", 0)
    issues = stats.get("issues", {}).get("totalCount", 0)
    repositories = stats.get("repositories", {}).get("totalCount", 0)
    
    # Normalize metrics - LOWER THRESHOLDS FOR BEGINNERS
    # 100+ commits = 100 points (instead of 500)
    commit_score = min(100, (commits / 100) * 100)
    # 20+ PRs = 100 points (instead of 100)
    pr_score = min(100, (pull_requests / 20) * 100)
    # 10+ issues = 100 points (instead of 50)
    issue_score = min(100, (issues / 10) * 100)
    # 5+ repos = 100 points (instead of 30)
    repo_score = min(100, (repositories / 5) * 100)
    
    # Weighted calculation - NO FOLLOWERS
    total_score = (
        (commit_score * 0.50) +
        (pr_score * 0.20) +
        (issue_score * 0.15) +
        (repo_score * 0.15)
    )
    
    # Determine grade - EASIER TO REACH HIGHER GRADES
    if total_score >= 85:
        grade = "A+"
    elif total_score >= 75:
        grade = "A"
    elif total_score >= 65:
        grade = "B+"
    elif total_score >= 55:
        grade = "B"
    elif total_score >= 45:
        grade = "C+"
    elif total_score >= 30:
        grade = "C"
    else:
        grade = "D"
    
    return grade, round(total_score, 2)

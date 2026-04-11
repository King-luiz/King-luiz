def calculate_grade(commits, pull_requests, issues, repositories, followers):
    # Define weights for metrics
    weights = {
        'commits': 0.4,
        'pull_requests': 0.3,
        'issues': 0.2,
        'repositories': 0.1
    }

    # Calculate total score
    total_score = (
        commits * weights['commits'] +
        pull_requests * weights['pull_requests'] +
        issues * weights['issues'] +
        repositories * weights['repositories']
    )

    # Determine grade based on total score
    if total_score >= 90:
        grade = 'A+'
    elif total_score >= 80:
        grade = 'A'
    elif total_score >= 70:
        grade = 'B+'
    elif total_score >= 60:
        grade = 'B'
    elif total_score >= 50:
        grade = 'C+'
    elif total_score >= 40:
        grade = 'C'
    else:
        grade = 'D'

    return grade

# Example usage:
if __name__ == '__main__':
    commits = 120
    pull_requests = 20
    issues = 5
    repositories = 10
    followers = 300
    grade = calculate_grade(commits, pull_requests, issues, repositories, followers)
    print(f'Developer grade: {grade}')
#!/usr/bin/python3

import requests

# TODO don't hardcode
maintainers = []

# Replace with your GitHub username, repository, and personal access token
# TODO don't hardcode, replace with env or 
repo_owner = ""
repository = ""
token = "" # TODO make optional, could replace with gh CLI auth

# Define the API endpoint for issues in the repository
api_url = f"https://api.github.com/repos/{repo_owner}/{repository}/issues"

# Create headers with the personal access token for authentication
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Initialize variables for pagination
page = 1
issues = []

while True:
    # Get the list of open issues for the current page
    params = {"page": page}
    response = requests.get(api_url, headers=headers, params=params)
    current_issues = response.json()

    # Add the issues from the current page to the list
    issues.extend(current_issues)

    # Check if there are more pages to fetch
    link_header = response.headers.get("Link")
    if not link_header or 'rel="next"' not in link_header:
        break  # No more pages

    page += 1

responded_issues = 0

# Iterate through the open issues and get the author of the latest comment
for issue in issues:
    issue_number = issue["number"]
    issue_url = issue["html_url"]  # Get the HTML URL of the issue
    comments_url = f"{api_url}/{issue_number}/comments"
    comments_response = requests.get(comments_url, headers=headers)
    comments = comments_response.json()
    
    if comments:
        latest_comment = comments[-1]  # The last comment is the latest one
        author = latest_comment["user"]["login"]
        if author in maintainers:
            responded_issues += 1
            continue
        print(f"Issue #{issue_number}: Latest Comment Author - {author}")
        print(f"   Issue Link: {issue_url}")
    else:
        print(f"Issue #{issue_number}: No comments")
        print(f"   Issue Link: {issue_url}")

print (f"Non-responded issues: {len(issues)-responded_issues}")

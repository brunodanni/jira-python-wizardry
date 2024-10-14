import requests
import csv
from requests.auth import HTTPBasicAuth

# Configure your Jira credentials and project details
JIRA_URL = "https://yourcompany.atlassian.net"  # Replace with your Jira URL
PROJECT_KEY = "AFJ"  # Replace with your project key
AUTH = HTTPBasicAuth("your_email@example.com", "your_api_token")  # Replace with your email and API token

def get_issues_from_project():
    # Construct the API URL for searching issues in the project
    url = f"{JIRA_URL}/rest/api/3/search"
    
    # Define the JQL query parameters to filter issues by project and fields to retrieve
    params = {"jql": f"project={PROJECT_KEY}", "fields": "id,key"}
    
    # Send a GET request to the Jira API to fetch issues
    response = requests.get(url, auth=AUTH, params=params)
    
    # Raise an exception if the response contains an HTTP error status
    response.raise_for_status()
    
    # Extract and return the list of issues from the JSON response
    return response.json().get('issues', [])

def get_comments_for_issue(issue_key):
    # Construct the API URL to fetch comments for a specific issue
    url = f"{JIRA_URL}/rest/servicedeskapi/request/{issue_key}/comment"
    
    # Send a GET request to the Jira API to fetch comments for the issue
    response = requests.get(url, auth=AUTH)
    
    # Raise an exception if the response contains an HTTP error status
    response.raise_for_status()
    
    # Extract and return the list of comments from the JSON response
    return response.json().get('values', [])

def filter_internal_comments(comments):
    # Initialize a list to store internal comments
    internal_comments = []
    
    # Iterate over each comment
    for comment in comments:
        # Check if the comment is internal (not public)
        if not comment.get('public', True):
            # Add the internal comment to the list
            internal_comments.append(comment)
    
    # Return the list of internal comments
    return internal_comments

def export_to_csv(comments, filename='internal_comments.csv'):
    # Define the CSV file headers based on the comment fields you want to include
    headers = ['issueKey', 'commentId', 'author', 'body', 'created']
    
    # Open a new CSV file for writing
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV dictionary writer object
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        # Write the header row to the CSV file
        writer.writeheader()
        
        # Iterate over each comment
        for comment in comments:
            # Write the comment data to the CSV file
            writer.writerow({
                'issueKey': comment.get('issueKey'),
                'commentId': comment.get('id'),
                'author': comment.get('author', {}).get('displayName', 'Unknown'),  # Display the author name
                'body': comment.get('body', ''),  # Assume body is a simple string
                'created': comment.get('created', '')  # Use the created date as a string
            })

def main():
    # Fetch all issues from the specified project
    issues = get_issues_from_project()
    
    # Initialize a list to store all internal comments
    all_internal_comments = []

    # Iterate over each issue
    for issue in issues:
        # Get the issue key (identifier)
        issue_key = issue['key']
        
        # Fetch comments for the current issue
        comments = get_comments_for_issue(issue_key)
        
        # Filter out only internal comments
        internal_comments = filter_internal_comments(comments)
        
        # Add the issue key to each internal comment for context
        for comment in internal_comments:
            comment['issueKey'] = issue_key
            
        # Add the internal comments to the list of all internal comments
        all_internal_comments.extend(internal_comments)

    # Export all internal comments to a CSV file
    export_to_csv(all_internal_comments, filename='internal_comments.csv')

if __name__ == "__main__":
    main()

# Attention: Every issue in the JSM project must have a request type assigned. Otherwise, the script will fail and return an HTTPError: 404 exception.

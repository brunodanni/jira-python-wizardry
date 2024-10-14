import requests
import json

# Define the Jira URL and credentials
JIRA_URL = "https://yourcompany.atlassian.net"  # Replace with your company's Jira URL
EMAIL = "your_email@example.com"  # Replace with your email
API_TOKEN = "your_api_token"  # Replace with your API token

def create_issue():
    # Construct the API endpoint URL for creating an issue
    url = f"{JIRA_URL}/rest/api/3/issue"

    # Prepare the headers, including authorization and content type
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(EMAIL, API_TOKEN)}",
        "Content-Type": "application/json"
    }

    # Define the issue details in JSON format
    issue_data = {
        "fields": {
            "project": {
                "key": "AFJ"  # Replace with your project key
            },
            "summary": "New issue created via Python",  # Brief title of the issue
            "description": "Description of the issue",  # Detailed description of the issue
            "issuetype": {
                "name": "Task"  # Replace with the desired issue type name (e.g., Bug, Story)
            }
        }
    }

    # Send a POST request to create the issue
    response = requests.post(url, headers=headers, data=json.dumps(issue_data))

    # Check if the request was successful
    if response.status_code == 201:
        # If successful, print the issue key of the newly created issue
        print("Issue created successfully!")
        print("Issue Key:", response.json()["key"])
    else:
        # If not successful, print the status code and response message
        print("Failed to create issue.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    create_issue()

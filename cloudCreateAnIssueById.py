import requests
from requests.auth import HTTPBasicAuth
import json

# Define the Jira API endpoint for creating issues
url = "https://yourcompany.atlassian.net/rest/api/3/issue"  # Replace with your Jira URL

# Set up authentication using email and API token
auth = HTTPBasicAuth("your_email@example.com", "your_api_token")  # Replace with your email and API token

# Define the headers for the HTTP request
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Define the payload with issue details in JSON format
payload = json.dumps({
    "fields": {
        "project": {
            "id": "10028"  # Replace with your actual project ID
        },
        "summary": "New issue created via Python",  # Brief title of the issue
        "description": {
            "content": [
                {
                    "content": [
                        {
                            "text": "Order entry fails when selecting supplier.",  # Detailed description of the issue
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        },
        "issuetype": {
            "id": "10006"  # Replace with the appropriate issue type ID for your project
        }
    }
})

# Send a POST request to create the issue
response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
)

# Print the response from the server in a formatted manner
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

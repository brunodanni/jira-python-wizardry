import requests
from requests.auth import HTTPBasicAuth
import json

# Authentication details
email = "your_email@example.com"
api_token = "your_api_token"
cloud_id = "your_cloud_id"

# Step 1: Create an issue

url_create_issue = "https://your-domain.atlassian.net/rest/api/3/issue"
auth = HTTPBasicAuth(email, api_token)
headers_create_issue = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
payload_create_issue = json.dumps({
    "fields": {
        "project": {
            "key": "YOUR_PROJECT_KEY"
        },
        "summary": "New issue created via API",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Creating an issue using the Jira API"
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "Task"
        }
    }
})
response_create_issue = requests.post(
    url_create_issue,
    data=payload_create_issue,
    headers=headers_create_issue,
    auth=auth
)

if response_create_issue.status_code == 201:
    issue_data = response_create_issue.json()
    issue_id_or_key = issue_data['key']  # or issue_data['id']
    print(f"Issue created successfully: {issue_id_or_key}")
else:
    print(f"Failed to create issue: {response_create_issue.status_code}, {response_create_issue.text}")
    exit()

# Step 2: Associate the form with the newly created issue

url_form = f"https://api.atlassian.com/jira/forms/cloud/{cloud_id}/issue/{issue_id_or_key}/form"
headers_form = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
payload_form = json.dumps({
    "formTemplate": {
        "id": "your_form_template_id"
    }
})
response_form = requests.post(
    url_form,
    data=payload_form,
    headers=headers_form,
    auth=auth
)
if response_form.status_code == 200:
    print("Form associated successfully.")
else:
    print(f"Failed to associate form: {response_form.status_code}, {response_form.text}")

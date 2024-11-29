import requests

# Jira Service Management Cloud base URL
base_url = "https://<your-instance>/rest/servicedeskapi"

# Your JSM Cloud API credentials
auth = ('email@example.com', 'api_token')

# List of organization names to create
organizations = ["OrgName1", "OrgName2"]

# Function to get the list of existing organizations
def get_existing_organizations():
    response = requests.get(f"{base_url}/organization", auth=auth)
    if response.status_code == 200:
        return response.json().get('values', [])
    else:
        print("Failed to retrieve existing organizations.")
        print(response.text)
        return []

# Get the list of existing organizations
existing_organizations = get_existing_organizations()

# Convert existing organization names to a set for easy lookup
existing_org_names = {org['name'] for org in existing_organizations}

for org_name in organizations:
    if org_name in existing_org_names:
        print(f"Organization '{org_name}' already exists.")
    else:
        response = requests.post(
            f"{base_url}/organization",
            json={"name": org_name},
            auth=auth
        )
        
        if response.status_code == 201:
            print(f"Successfully created organization: {org_name}")
            print(response.json())
        else:
            print(f"Failed to create organization: {org_name}")
            print(response.text)

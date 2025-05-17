# United States African Development Foundation (USADF) Developer Resources

## API Reference

The ADF API provides programmatic access to the AI-powered system. This reference outlines the key endpoints, authentication methods, and usage patterns.

### Authentication

All API requests require authentication using JWT tokens:

```bash
# Request an access token
curl -X POST https://api.adf.us.gov-ai.co/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id": "YOUR_CLIENT_ID", "client_secret": "YOUR_CLIENT_SECRET"}'
```

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/grants/opportunities` | GET | Retrieve available grant programs |
| `/grants/applications` | POST | Submit grant applications |
| `/projects/status` | GET | Monitor project implementation status |
| `/projects/outcomes` | GET | Analyze project outcomes and impact |

### Example Integration

```python
import requests
import json

# Configuration
API_BASE_URL = 'https://api.adf.us.gov-ai.co'
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

# Authenticate and get token
def get_token():
    auth_url = f"{API_BASE_URL}/auth/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(auth_url, json=payload)
    return response.json()['access_token']

# Make authenticated request
def api_request(endpoint, method='GET', data=None):
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = f"{API_BASE_URL}{endpoint}"
    
    if method == 'GET':
        response = requests.get(url, headers=headers, params=data)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    
    return response.json()

# Example: Retrieve active grant programs
grants = api_request(
    endpoint='/grants/opportunities',
    method='GET',
    data={
        'status': 'active',
        'categories': ['economic_development', 'education'],
        'min_amount': 50000,
        'limit': 10
    }
)

print(f"Found {len(grants['results'])} grant programs")
for grant in grants['results']:
    print(f"- {grant['title']} (Amount: ${grant['amount']:,.2f})")
```

## SDK Libraries

Official client libraries are available for multiple languages:

- **Python**: `pip install hms-nfo-adf-client`
- **JavaScript**: `npm install @hms-nfo/adf-client`
- **Java**: Available through Maven Central
- **Go**: `go get github.com/hms-nfo/adf-client`

## Documentation Resources

- [Complete API Reference](https://developers.adf.us.gov-ai.co/api)
- [Code Samples Repository](https://github.com/hms-nfo/adf-examples)
- [Developer Community Forum](https://community.adf.us.gov-ai.co/developers)
- [Integration Tutorials](https://developers.adf.us.gov-ai.co/tutorials)

[Back to Index](index.md)
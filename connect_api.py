import requests

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

def get_access_token():
    resp = requests.post(
        "https://api.petfinder.com/v2/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

ACCESS_TOKEN = get_access_token()

def fetch_pets(type: str, breed: str = None, location: str = None, limit: int = 20):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"type": type, "limit": limit}
    if breed: params["breed"] = breed
    if location: params["location"] = location

    resp = requests.get("https://api.petfinder.com/v2/animals", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json().get("animals", [])

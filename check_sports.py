import requests

API_KEY = "your_api_key_here"

response = requests.get(
    "https://api.the-odds-api.com/v4/sports",
    params={"apiKey": API_KEY}
)

print(response.json())
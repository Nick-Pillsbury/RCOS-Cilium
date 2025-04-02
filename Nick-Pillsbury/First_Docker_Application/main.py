import requests

response = requests.get("https://official-joke-api.appspot.com/random_joke")
joke = response.json()
print(f"{joke['setup']} - {joke['punchline']}")
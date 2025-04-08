import requests
import dotenv
import os

# Load API key from Secret .env file
dotenv.load_dotenv()
api_key = os.getenv("RIOT_API_KEY")
if not api_key:
    raise ValueError("API key not found. Check your .env file.")

# Headers for Calling the Riot API
headers = {
    "X-Riot-Token": api_key,
    "User-Agent": "MyRiotApp/1.0"
}


def Get_Player_By_ID(summoner_name: str, tag_line: str) -> dict:
    # Make the Url to call this command in Riot API
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
    
    # Make request
    response = requests.get(url, headers=headers)

    # Hnadle the response
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    else:
        return response.json()

    
def Get_Player_By_PUID(puid: str) -> dict:
    # Make Url to call this command in the riot api
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puid}"
    
    # make Request
    response = requests.get(url, headers=headers)

    # handle response
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    else:
        return response.json()


def Get_Recent_Match_IDs(puuid: str, count: int = 20) -> list:
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    return response.json()


def Get_Match_Details(match_id: str) -> dict:
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    return response.json()
 
 
def Get_Summoner_Stats(puuid: str) -> dict:
    url = f"https://americas.api.riotgames.com/lol/league/v4/entries/by-account/{puuid}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    return response.json()
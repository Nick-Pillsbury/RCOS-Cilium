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
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puid}"
    response = requests.get(url, headers=headers)
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





#####################################
##########     Method1     ##########
#####################################


def Recent_Match_History(summoner_name: str, tag_line: str, count: int = 20) -> dict:
    # Get PUUID from summoner name
    player_data = Get_Player_By_ID(summoner_name, tag_line)
    puuid = player_data.get("puuid")
    if not puuid:
        return {"status": "Error", "message": "Player not found."}

    # Get recent match IDs
    match_ids = Get_Recent_Match_IDs(puuid, count)
    if not match_ids:
        return {"status": "Error", "message": "No recent matches found."}
    
    # Initialize variables for stats
    total_kills = total_deaths = total_assists = wins = 0
    champion_stats = {}
    match_details_list = []
    
    # Get details for each match and calculate stats
    for match_id in match_ids:
        match_data = Get_Match_Details(match_id)
        participants = match_data["info"]["participants"]
        
        # Find the player's stats in the match
        for participant in participants:
            if participant["puuid"] == puuid:
                kills = participant["kills"]
                deaths = participant["deaths"]
                assists = participant["assists"]
                total_kills += kills
                total_deaths += deaths
                total_assists += assists
                
                # Champion stats
                champion_name = participant["championName"]
                if champion_name not in champion_stats:
                    champion_stats[champion_name] = {"games": 0, "wins": 0}
                champion_stats[champion_name]["games"] += 1
                if participant["win"]:
                    champion_stats[champion_name]["wins"] += 1
                
                match_details = {
                    "gameMode": match_data["info"]["gameMode"],
                    "gameDuration": match_data["info"]["gameDuration"],
                    "champion": champion_name,
                    "outcome": "Win" if participant["win"] else "Loss",
                    "kills": kills,
                    "deaths": deaths,
                    "assists": assists
                }
                match_details_list.append(match_details)
                if participant["win"]:
                    wins += 1
    
    # Calculate Win Rate and KDA
    win_rate = (wins / len(match_ids))
    kda = (total_kills + total_assists) / total_deaths if total_deaths != 0 else total_kills + total_assists
    
    # Summarize all the stats
    summary = {
        "summonerName": summoner_name,
        "tagLine": tag_line,
        "winRate": round(win_rate, 2),
        "kda": round(kda, 2),
        "recentMatches": match_details_list,
        "championStats": champion_stats
    }

    return summary




#####################################
##########     Method2     ##########
#####################################


def Get_Champion_Mastery(name: str, tag: str) -> dict:
    # get the puuid
    player_data = Get_Player_By_ID(name, tag)
    puuid = player_data.get("puuid")
    if not puuid:
        return {"status": "Error", "message": "Player not found."}
    
    # make the call
    url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    response = requests.get(url, headers=headers)
    
    # handle the response
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    
    mastery_data = response.json()
    champion_mastery = [{"championId": cm["championId"], "championPoints": cm["championPoints"]} for cm in mastery_data]
    return {"summonerName": name, "tagLine": tag, "championMastery": champion_mastery}



#####################################
##########     Method3     ##########
#####################################


def Get_player_rank_info(name: str, tag: str) -> dict:
    # get the puuid
    player_data = Get_Player_By_ID(name, tag)
    puuid = player_data.get("puuid")
    if not puuid:
        return {"status": "Error", "message": "Player not found."}
    
    # make call to riot api
    url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    response = requests.get(url, headers=headers)
    
    # handle response
    if response.status_code != 200:
        return {"status": "Error", "code": response.status_code, "reason": response.reason}
    
    rank_data = response.json()
    rank_info = [{"queueType": rank["queueType"], "tier": rank["tier"], "rank": rank["rank"], "leaguePoints": rank["leaguePoints"]} for rank in rank_data]
    return {"summonerName": name, "tagLine": tag, "rank": rank_info}
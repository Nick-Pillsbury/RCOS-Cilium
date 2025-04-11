import requests
import json


def Method1():
    url = "https://rcos-latest.onrender.com/recent-match-history/Marxador/Karl/25"
    print(f"\nRequesting: {url}")
    response = requests.get(url)
    response.raise_for_status()
    try:
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    print("SummonerName:",data["summonerName"])
    print("TagLine:",data["tagLine"])
    print("WinRate:",data["winRate"])
    print("Kda:",data["kda"])
    
    print("\nRecent Matches: ")
    for x in range(len(data["recentMatches"])):
        print(f"Game: {x+1}")
        print(data["recentMatches"][x])
    
    print("\nChampion Stats: ")
    print(data["championStats"])


def Method2():
    url = "https://rcos-latest.onrender.com/champion-mastery/Marxador/Karl"
    print(f"\nRequesting: {url}")
    response = requests.get(url)
    response.raise_for_status()
    try:
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    print("SummonerName:",data["summonerName"])
    print("TagLine:",data["tagLine"])
    
    print("\nChampion Mastery:")
    for x in range(len(data["championMastery"])):
        print(data["championMastery"][x])


def Method3():
    url = "https://rcos-latest.onrender.com/rank_info/Marxador/Karl"
    print(f"\nRequesting: {url}")
    response = requests.get(url)
    response.raise_for_status()
    try:
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    print("SummonerName:",data["summonerName"])
    print("TagLine:",data["tagLine"])
    print("Rank Info:")
    print(data["rank"])


def Method4():
    url = "https://rcos0-latest.onrender.com/CharJoke"
    print(f"\nRequesting: {url}")
    response = requests.get(url)
    response.raise_for_status()
    try:
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    
    print(data["joke"])


Method1()
Method2()
Method3()
Method4()
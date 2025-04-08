from fastapi import FastAPI
from riot import get_summoner_by_name, get_ranked_stats, get_recent_matches

app = FastAPI()

@app.get("/matches/{name}/{tag}")
def summoner_info(name: str):
    
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from riot import Recent_Match_History, Get_Champion_Mastery, Get_player_rank_info


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
        <head>
            <title>Riot FastAPI</title>
        </head>
        <body>
            <h1>Hi!</h1>
            <p>address/recent-match-history/{name}/{tag}/{count} - Gives a summary of player's x most recent games</p>
            <p>address/champion-mastery/{name}/{tag} - Gives a player's champion mastery</p>
            <p>address/rank_info/{name}/{tag} - Gives a player's current rank</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/recent-match-history/{name}/{tag}/{count}", response_model=dict)
def recent_match_history(name: str, tag: str, count: int = 20):
    try:
        player_summary = Recent_Match_History(name, tag, count)
        
        if "status" in player_summary and player_summary["status"] == "Error":
            raise HTTPException(status_code=404, detail=player_summary["message"])
        return player_summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/champion-mastery/{name}/{tag}", response_model=dict)
def champion_mastery(name: str, tag: str):
    try:
        player_mastery = Get_Champion_Mastery(name, tag)
        
        if "status" in player_mastery and player_mastery["status"] == "Error":
            raise HTTPException(status_code=404, detail=player_mastery["message"])
        return player_mastery

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@app.get("/rank_info/{name}/{tag}", response_model=dict)
def player_rank(name: str, tag: str):
    try:
        player_rank = Get_player_rank_info(name, tag)
        
        if "status" in player_rank and player_rank["status"] == "Error":
            raise HTTPException(status_code=404, detail=player_rank["message"])
        return player_rank

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
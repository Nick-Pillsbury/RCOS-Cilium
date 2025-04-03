import cowsay
import random
import requests
from fastapi import FastAPI


app = FastAPI()


# Define the endpoint that returns a random joke
@app.get("/CharJoke")
def get_joke():
    
    joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    joke_text = f"{joke['setup']} - {joke['punchline']}"
    cow_say_output = cowsay.get_output_string(random.choice(cowsay.char_names), joke_text)
    
    # Return it as a API Response
    return {"joke": cow_say_output}
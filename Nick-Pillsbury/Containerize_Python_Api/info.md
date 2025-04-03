# Containerizing a Python Api in Docker

---

## Goal
The goal of this is to containerize a python Api.

---


### Step 1: Create A Basic Api With FastApi and Uvicorn
#### Main.py
Using FastApi Create a simple Api with at least one method.
```python
import cowsay
import random
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/CharJoke")
def get_joke():

    joke = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    joke_text = f"{joke['setup']} - {joke['punchline']}"
    cow_say_output = cowsay.get_output_string(random.choice(cowsay.char_names), joke_text)

    return {"joke": cow_say_output}
```

#### Locally Testing Your Api
```bash
# Host with Uvicorn Locally
uvicorn main:app --host 0.0.0.0 --port 8000

# In a new terminal (Use your actual ip4 address)
# Or don't specify a port / host to get the deafult of your machine
curl http://IPAddress/FunctionName
```

---

### Step 2: Create a Dockerfile
A `Dockerfile` is a blueprint for your containerized application.

```dockerfile
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install uvicorn cowsay requests fastapi

# Expose the port FastAPI will run on in the container
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn Local host, port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### Step 3: Build and Run Your Docker Application
```bash
# Build the Docker image (-t specifies the image name)
# . specifies the current directory
docker build -t fastapi-app .

# Run the container
# -d detached mode -in background
# -p maps port on machine to port in container
docker run -d -p 8000:8000 fastapi-app
```

---

### Step 4: Test It Out
Find Your local ip4 address.
We set it to listen on 0.0.0.0, which is any device on your local network.
```bash
ipconfig
curl http://Ip4Address:8000/FunctionName
```

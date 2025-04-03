# Containerizing a Python Script

---

## Goal
The goal of this project is to containerize a Python script using Docker. This will allow the script to run in a consistent environment, independent of the host machine's configuration.

---

## Why is this Useful?
Containerizing a Python script offers several advantages:

- **Portability**: The script runs the same way on any system, eliminating compatibility issues.
- **Dependency Management**: Ensures the script uses the correct versions of libraries without conflicts.
- **Easy Deployment**: No need to manually install dependencies—just run the container.
- **Isolation**: Keeps the script separate from the host system, preventing unintended interactions.
- **Scalability & Reproducibility**: Enables easier scaling and consistent execution in CI/CD pipelines.

---

## What You Will Learn
By completing this project, you will gain experience with:

- Writing a `Dockerfile` to define a containerized environment.
- Managing dependencies using `requirements.txt`.
- Building and running a Docker container.
- Understanding containerization concepts and best practices.

<br>
<br>
<br>

## Steps to Containerize a Python Script

---

### Step 1: Create Your Python Script
Write a Python script (`main.py`) that you want to containerize. Ensure it does not require user input to avoid issues when running in a container.

---


### Step 2: Create a Dockerfile
A `Dockerfile` is a blueprint for your containerized application.

```dockerfile
# Use the official Python 3.9 image
FROM python:3.9

# Add Our python script and add it to the main directory
ADD main.py .

# Install required Python packages
RUN pip install requests

# Define the command to run the script
CMD ["python", "./main.py"]
```

---

### Step 3: Build and Run Your Docker Application

```bash
# Build the Docker image (-t specifies the image name)
# . specifies the current directory
docker build -t project-name .

# Run the container
docker run project-name
```
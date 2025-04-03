FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install uvicorn cowsay requests fastapi

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn Local host, port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.8-slim

# dependencies
RUN pip install Flask prometheus_client iperf3

# code into the container
COPY iperfjson.py /app/iperfjson.py

# Set  working directory
WORKDIR /app

# Expose  port 
EXPOSE 8020

# Command to run the application
CMD ["python3", "iperfjson.py"]
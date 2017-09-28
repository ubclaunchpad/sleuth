# Use python:3 as the base Docker image
FROM python:3
# Set current working directory in the container
WORKDIR /home/sleuth
# Copy requirements into the docker container
COPY requirements.txt ./
# Install required Python packages
RUN pip install -r requirements.txt
# Copy the contents of the current working directory to the container
COPY . .
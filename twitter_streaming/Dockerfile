# Base Images
FROM python:3.9.5-slim-buster

# Set the working directory in the container
WORKDIR /twitter_streaming

# Copy Source files to the container
COPY ./* /twitter_streaming

# Upgrade Pip and Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Copy the current directory contents into the container
COPY . /service

# Install any needed packages specified in requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r service/requirements.txt

# Set the working directory
WORKDIR /service/app

# Run script when the container launches
CMD ["python", "main.py"]
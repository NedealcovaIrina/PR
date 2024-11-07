# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install flask mysql-connector-python

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=main2.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the command to start the Flask app
CMD ["flask", "run"]

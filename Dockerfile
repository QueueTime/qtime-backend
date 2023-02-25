# Set base image (host OS)
FROM python:3.9-slim-bullseye

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /src

# Set the environment for app to run
ENV ENV=prod

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Update pip and install dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the content of the local directory to the working directory
COPY . .

# Command to run on container start
CMD [ "python", "manage.py" ]
# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /website/app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP main.py
ENV DEBUG false

EXPOSE 5007

# Run app.py when the container launches
CMD ["flask", "run","--host=0.0.0.0", "--port=5007"]
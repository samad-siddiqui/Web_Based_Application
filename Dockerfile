# Use the official Python image as base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Run the installation
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire core project into the container
COPY . .

# Expose the port that Django runs on
EXPOSE 8000

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

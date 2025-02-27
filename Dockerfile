# Use a specific version of Python for compatibility
FROM python:3.12

# Set environment variable to disable buffering for easy logging

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port for the app to be accessible
EXPOSE 8000

# Run migrations and collect static files, then start the server using Gunicorn
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
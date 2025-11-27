# Use Python 3.12 official slim image
FROM python:3.12-slim

# Install system dependencies (awscli optional)
RUN apt update -y && apt install -y awscli

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Command to run the app
#CMD ["python3", "app.py"]
CMD ["streamlit","run","stm.py"]
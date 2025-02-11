# Use Python 3.10 slim image as the base
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies and remove cache to slim down image size
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit will run on
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Set entrypoint to run Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

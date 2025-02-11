# Use Python 3.10 slim image as the base
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the entire application
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV HOST=0.0.0.0

# Command to run the application
CMD streamlit run app.py --server.port=$PORT --server.address=$HOST 
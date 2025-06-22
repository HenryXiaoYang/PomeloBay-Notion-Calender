FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies
RUN pip3 install --upgrade pip

# Copy application files
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port for the FastAPI server
EXPOSE 3030

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3030", "--log-config", "log_config.yaml"]
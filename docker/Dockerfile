# Use the official Python Alpine base
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    python3 python3-dev py3-pip build-base \
    libffi-dev openssl-dev cargo gcc musl-dev postgresql-dev \
    postgresql-client

# Install uv
RUN pip install uv

# Copy your project files (only pyproject.toml and lock files first for caching!)
COPY pyproject.toml uv.lock ./

# Install deps using uv
RUN uv sync

# Copy 
COPY . .

# Expose port
EXPOSE 8000

# Install
# RUN uv run python manage.py migrate

# Start Django using uv
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

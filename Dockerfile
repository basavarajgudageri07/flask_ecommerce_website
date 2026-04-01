# -------- Stage 1: Build Stage --------
FROM python:3.8 AS builder

WORKDIR /app

# Copy project files
COPY . .

# Install dependencies in a separate folder
RUN pip install --upgrade pip && \
    pip install flask --prefix=/install

# -------- Stage 2: Final Runtime --------
FROM python:3.9-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations && python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput


# Expose the port Django will run on
EXPOSE 8000

# Start server
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
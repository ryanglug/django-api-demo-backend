FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    libpq-dev

COPY requirements.txt .
COPY Makefile .
RUN make deps

COPY . .

RUN make lint
RUN make test


# Collect static files
RUN python manage.py collectstatic --noinput


# Expose the port Django will run on
EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]

# Start server
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
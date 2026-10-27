FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* # Clean up apt cache to reduce image size

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

# make the entrypoint executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Make the Tailwind binary executable
RUN chmod +x ./tailwindcss-linux-x64

ENTRYPOINT ["/app/entrypoint.sh"]
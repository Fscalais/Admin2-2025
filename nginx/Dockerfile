FROM nginx:1.27
RUN apt-get update && apt-get install -y --no-install-recommends \
      certbot python3-certbot-nginx ca-certificates \
    && rm -rf /var/lib/apt/lists/*

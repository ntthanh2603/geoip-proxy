# Use Python slim image
FROM python:3.11-slim

# Define build arguments
ARG GEOIPUPDATE_ACCOUNT_ID
ARG GEOIPUPDATE_LICENSE_KEY

# Set environment variables from build arguments
ENV GEOIPUPDATE_ACCOUNT_ID=$GEOIPUPDATE_ACCOUNT_ID
ENV GEOIPUPDATE_LICENSE_KEY=$GEOIPUPDATE_LICENSE_KEY
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install geoipupdate and necessary tools
RUN apt-get update \
    && apt-get install -y wget ca-certificates jq curl \
    && export GEOIPUPDATE_VERSION=$(curl -s https://api.github.com/repos/maxmind/geoipupdate/releases/latest | jq -r '.tag_name') \
    && wget -O /tmp/geoipupdate.deb "https://github.com/maxmind/geoipupdate/releases/download/${GEOIPUPDATE_VERSION}/geoipupdate_${GEOIPUPDATE_VERSION#v}_linux_amd64.deb" \
    && dpkg -i /tmp/geoipupdate.deb \
    && rm /tmp/geoipupdate.deb \
    && rm -rf /var/lib/apt/lists/*

# Create directories for GeoIP databases
RUN mkdir -p /usr/share/GeoIP /tmp/geoip

# Copy GeoIP configuration and download databases
COPY geoip.conf /etc/GeoIP.conf
RUN sed -i "s/\$GEOIPUPDATE_ACCOUNT_ID/${GEOIPUPDATE_ACCOUNT_ID}/g" /etc/GeoIP.conf && \
    sed -i "s/\$GEOIPUPDATE_LICENSE_KEY/${GEOIPUPDATE_LICENSE_KEY}/g" /etc/GeoIP.conf
RUN /usr/bin/geoipupdate

# Copy databases to temp location so they can be copied to volume on startup
RUN cp -r /usr/share/GeoIP/* /tmp/geoip/

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src src
COPY main.py .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PORT=4360

EXPOSE ${PORT}

ENTRYPOINT ["/entrypoint.sh"]

#!/bin/bash

# Copy GeoIP databases to mounted volume if they don't exist
if [ ! -f "/usr/share/GeoIP/GeoLite2-City.mmdb" ]; then
    echo "Copying GeoIP databases to mounted volume..."
    cp -r /tmp/geoip/* /usr/share/GeoIP/ 2>/dev/null || echo "No databases to copy from /tmp/geoip"
fi

# Start the API server
echo "Starting API server..."
python main.py

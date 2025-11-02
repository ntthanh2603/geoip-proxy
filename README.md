# GeoIP Proxy

A lightweight FastAPI service that provides IP geolocation data using MaxMind's GeoLite2 databases.

## Features

- 🌍 IP geolocation lookup with detailed information
- 🔄 Automatic daily database updates from MaxMind
- 🐳 Docker deployment ready
- 🚀 Fast FastAPI backend
- 📊 Bulk IP lookup support

## API Endpoints

### Get Client IP

```
GET /
```

Returns the client's IP address.

### Single IP Lookup

```
GET /{ip}
```

Returns detailed geolocation information for a single IP address.

**Example:**

```
GET /8.8.8.8
```

### Bulk IP Lookup

```
GET /bulk/{ips}
```

Returns geolocation information for multiple IP addresses (comma-separated).

**Example:**

```
GET /bulk/8.8.8.8,1.1.1.1
```

## Response Format

```json
{
  "query": "8.8.8.8",
  "status": "success",
  "continent": "North America",
  "continentCode": "NA",
  "country": "United States",
  "countryCode": "US",
  "region": "CA",
  "regionName": "California",
  "city": "Mountain View",
  "district": "",
  "zip": "94035",
  "lat": 37.386,
  "lon": -122.0838,
  "timezone": "America/Los_Angeles",
  "offset": 5,
  "currency": "USD",
  "isp": "Google LLC",
  "org": "Google LLC",
  "as": "AS15169 Google LLC",
  "asname": "Google LLC"
}
```

## Setup

### Prerequisites

1. Get a MaxMind license key:

   - Sign up at https://www.maxmind.com/en/geolite2/signup
   - Generate a license key
   - Note your Account ID and License Key

2. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your MaxMind credentials:
   ```
   PORT=4360
   GEOIPUPDATE_ACCOUNT_ID=your_account_id
   GEOIPUPDATE_LICENSE_KEY=your_license_key
   ```

### Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:

   ```bash
   python main.py
   ```

3. Access the API:
   - API: http://localhost:4360
   - Docs: http://localhost:4360/docs
   - ReDoc: http://localhost:4360/redoc

### Docker Deployment

1. Build and run with docker-compose:

   ```bash
   docker-compose up --build
   ```

2. The service will be available at `http://localhost:4360`

## Project Structure

```
geoip-proxy/
├── src/
│   ├── app.py                    # FastAPI application
│   ├── configs/
│   │   └── path_database.py      # Database path configuration
│   ├── controlers/
│   │   └── geoip_controler.py    # API endpoints
│   ├── services/
│   │   └── geoip_service.py      # GeoIP lookup logic
│   └── types/
│       └── ip_geolocaltion.py    # Data models
├── main.py                       # Entry point
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose configuration
├── entrypoint.sh                 # Container entrypoint
├── geoip.conf                    # GeoIP update configuration
├── requirements.txt              # Python dependencies
└── .env.example                  # Environment variables template
```

## Technologies

- **FastAPI** - Modern Python web framework
- **MaxMind GeoLite2** - IP geolocation databases
- **Docker** - Containerization
- **uvicorn** - ASGI server

## License

This project uses the GeoLite2 data created by MaxMind, available from [MaxMind](https://www.maxmind.com).

## Support

For support, please open an issue on the [GitHub repository](https://github.com/ntthanh2603/geoip-proxy/issues).

# GeoIP Proxy

[![Daily Docker Build](https://github.com/ntthanh2603/geoip-proxy/actions/workflows/docker-build.yml/badge.svg)](https://github.com/ntthanh2603/geoip-proxy/actions/workflows/docker-build.yml)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue?logo=docker)](https://github.com/ntthanh2603/geoip-proxy/pkgs/container/geoip-proxy)
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-00a393?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A lightweight FastAPI service that provides IP geolocation data using MaxMind's GeoLite2 databases.

## ✨ Features

- 🌍 **IP Geolocation Lookup** - Detailed location data for any IP address
- 🔄 **Daily Auto Updates** - GeoIP databases refreshed daily via GitHub Actions
- 🐳 **Docker Ready** - Pre-built images on GitHub Container Registry
- 🚀 **Fast API** - Built with FastAPI for high performance
- 📊 **Bulk Lookup** - Query multiple IPs in a single request
- 📚 **Auto Documentation** - Swagger UI and ReDoc included
- 🔒 **Type Safe** - Full Pydantic validation

## 🚀 Quick Start

### Using Docker (Recommended)

Pull and run the pre-built image from GitHub Container Registry:

```bash
docker pull ghcr.io/ntthanh2603/geoip-proxy:latest
docker run -p 4360:4360 -e PORT=4360 ghcr.io/ntthanh2603/geoip-proxy:latest
```

Access the API at: **http://localhost:4360**

### Using Docker Compose

```bash
git clone https://github.com/ntthanh2603/geoip-proxy.git
cd geoip-proxy
cp .env.example .env
# Edit .env with your MaxMind credentials
docker-compose up -d
```

## 📡 API Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Get client's IP address | `curl http://localhost:4360/` |
| `/{ip}` | GET | Lookup single IP | `curl http://localhost:4360/8.8.8.8` |
| `/bulk/{ips}` | GET | Lookup multiple IPs | `curl http://localhost:4360/bulk/8.8.8.8,1.1.1.1` |
| `/docs` | GET | Swagger UI documentation | Open in browser |
| `/redoc` | GET | ReDoc documentation | Open in browser |

## 📄 Response Format

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

## 🛠️ Development Setup

### Prerequisites

Get a MaxMind license key (free):
- Sign up: https://www.maxmind.com/en/geolite2/signup
- Generate license key: https://www.maxmind.com/en/accounts/current/license-key

### Local Development

```bash
# Clone repository
git clone https://github.com/ntthanh2603/geoip-proxy.git
cd geoip-proxy

# Configure environment
cp .env.example .env
# Edit .env with your MaxMind credentials

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Access the API:
- **API:** http://localhost:4360
- **Swagger UI:** http://localhost:4360/docs
- **ReDoc:** http://localhost:4360/redoc

### Docker Development

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```


## 📦 GitHub Container Registry

Pre-built Docker images with daily updated GeoIP databases are available at:
**[ghcr.io/ntthanh2603/geoip-proxy](https://github.com/ntthanh2603/geoip-proxy/pkgs/container/geoip-proxy)**

### Available Tags

| Tag | Description | Update Frequency |
|-----|-------------|------------------|
| `latest` | Latest stable build | On every push to main |
| `YYMMDD` | Daily snapshot | Daily at 00:00 UTC |
| `main-<sha>` | Specific commit | On demand |

### Usage

```bash
# Latest version
docker pull ghcr.io/ntthanh2603/geoip-proxy:latest

# Specific date (e.g., Nov 2, 2025)
docker pull ghcr.io/ntthanh2603/geoip-proxy:251102
```

## ⚙️ GitHub Actions

### Automated Workflows

| Workflow | Schedule | Purpose |
|----------|----------|---------|
| **Daily Docker Build** | Daily at 00:00 UTC | Update GeoIP databases & build images |

### Setup GitHub Actions

To enable automated builds:

1. Navigate to: **Settings** → **Secrets and variables** → **Actions**
2. Add repository secrets:

```
Name: GEOIPUPDATE_ACCOUNT_ID
Value: <your_maxmind_account_id>

Name: GEOIPUPDATE_LICENSE_KEY
Value: <your_maxmind_license_key>
```

3. Go to **Actions** tab → Select workflow → **Run workflow**

The workflow will:
- ✅ Verify secrets
- ✅ Download latest GeoIP databases
- ✅ Build Docker image
- ✅ Push to GitHub Container Registry

## 📂 Project Structure

```
geoip-proxy/
├── .github/workflows/          # CI/CD workflows
│   └── docker-build.yml        # Daily build automation
├── src/
│   ├── app.py                  # FastAPI application
│   ├── configs/
│   │   └── path_database.py    # Database path config
│   ├── controlers/
│   │   └── geoip_controler.py  # API endpoints
│   ├── services/
│   │   └── geoip_service.py    # GeoIP lookup logic
│   └── types/
│       └── ip_geolocaltion.py  # Pydantic models
├── main.py                     # Entry point
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Compose configuration
├── requirements.txt            # Python dependencies
└── .env.example                # Environment template
```

## 🛠️ Technologies

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Modern Python web framework |
| **MaxMind GeoLite2** | IP geolocation databases |
| **Pydantic** | Data validation |
| **Docker** | Containerization |
| **GitHub Actions** | CI/CD automation |

## 📝 License

This project uses GeoLite2 data created by MaxMind, available from [MaxMind](https://www.maxmind.com).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/ntthanh2603/geoip-proxy/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ntthanh2603/geoip-proxy/discussions)

---

<div align="center">

**[⭐ Star this repo](https://github.com/ntthanh2603/geoip-proxy)** if you find it useful!

Made with ❤️ using FastAPI and MaxMind GeoLite2

</div>

from fastapi import FastAPI
from src.controlers.geoip_controler import geoip_router

# Create application
app = FastAPI(title="GeoIP Proxy",
              description="GeoIP Proxy API",
              version="1.0.0",
              docs_url="/docs",
              redoc_url="/redoc")


# Include router
app.include_router(geoip_router)

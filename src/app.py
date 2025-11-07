from fastapi import FastAPI
from src.controlers.geoip_controler import geoip_router
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-7s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Reduce noise from uvicorn
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Create application
app = FastAPI(
    title="GeoIP Server",
    description="GeoIP Server API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 GeoIP Server started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 GeoIP Server stopped")


# Include router
app.include_router(geoip_router)

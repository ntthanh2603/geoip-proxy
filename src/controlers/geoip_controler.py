from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from typing import Union, Dict, List
from src.services.geoip_service import geoip_service
from src.types.ip_geolocaltion import IPGeoLocation
import logging
import re

logger = logging.getLogger(__name__)
geoip_router = APIRouter()

# Simple IP validation regex
IP_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$|^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$')


@geoip_router.get("/")
async def get_client_ip(request: Request) -> Dict[str, str]:
    """Get the client's IP address"""
    return {"ip": request.client.host if request.client else None}


@geoip_router.get("/favicon.ico")
async def favicon():
    """Return 204 No Content for favicon requests"""
    return Response(status_code=204)


@geoip_router.get("/bulk/{ips}")
async def lookup_bulk_ips(ips: str) -> List[Union[IPGeoLocation, Dict[str, str]]]:
    """Lookup geolocation for multiple IPs (comma-separated)"""
    ip_list = [ip.strip() for ip in ips.split(",")]
    return [geoip_service.lookup(ip) for ip in ip_list]


@geoip_router.get("/{ip}")
async def lookup_ip(ip: str) -> Union[IPGeoLocation, Dict[str, str]]:
    """Lookup geolocation for a single IP address"""
    if not IP_PATTERN.match(ip):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid IP address format"}
        )
    return geoip_service.lookup(ip)

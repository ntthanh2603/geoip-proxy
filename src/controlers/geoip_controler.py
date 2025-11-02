from fastapi import APIRouter, Request
from typing import Union, Dict, List
from src.services.geoip_service import geoip_service
from src.types.ip_geolocaltion import IPGeoLocation

# Create router for geoip
geoip_router = APIRouter()


@geoip_router.get("/")
async def get_client_ip(request: Request) -> Dict[str, str]:
    """
    Get the client's IP address

    Returns:
        dict: Client IP address
    """
    # Get client IP from request
    client_ip = request.client.host if request.client else None
    return {"ip": client_ip}


@geoip_router.get("/{ip}", response_model=Union[IPGeoLocation, Dict[str, str]])
async def lookup_ip(ip: str) -> Union[IPGeoLocation, Dict[str, str]]:
    """
    Lookup geolocation information for a single IP address

    Args:
        ip: IP address to lookup

    Returns:
        IPGeoLocation or error dict: Geolocation information
    """
    return geoip_service.lookup(ip)


@geoip_router.get("/bulk/{ips}")
async def lookup_bulk_ips(ips: str) -> List[Union[IPGeoLocation, Dict[str, str]]]:
    """
    Lookup geolocation information for multiple IP addresses

    Args:
        ips: Comma-separated list of IP addresses

    Returns:
        list: List of geolocation information for each IP
    """
    ip_list = ips.split(",")
    results = [geoip_service.lookup(ip.strip()) for ip in ip_list]
    return results

import maxminddb
import os
import time
import logging
from typing import Optional, Dict, Union
from src.configs.path_database import PATH_DATABASE
from src.types.ip_geolocaltion import IPGeoLocation

logger = logging.getLogger(__name__)


class GeoIPService:
    """Service for looking up IP geolocation using MaxMind databases"""

    def __init__(self):
        self.lookup_city: Optional[maxminddb.Reader] = None
        self.lookup_country: Optional[maxminddb.Reader] = None
        self.lookup_asn: Optional[maxminddb.Reader] = None
        self.sync_database()

    def sync_database(self):
        """Load all GeoIP databases"""
        logger.info("Loading GeoIP databases...")
        self.lookup_city = self.load_database(os.path.join(PATH_DATABASE, "GeoLite2-City.mmdb"))
        self.lookup_country = self.load_database(os.path.join(PATH_DATABASE, "GeoLite2-Country.mmdb"))
        self.lookup_asn = self.load_database(os.path.join(PATH_DATABASE, "GeoLite2-ASN.mmdb"))
        logger.info("✓ All databases loaded")

    def load_database(self, path: str) -> maxminddb.Reader:
        """Load a MaxMind database with retry logic"""
        database_name = os.path.basename(path)
        retry_count = 0

        while True:
            try:
                return maxminddb.open_database(path)
            except Exception as error:
                retry_count += 1
                logger.warning(f"{database_name} failed (attempt #{retry_count}): {error}")
                time.sleep(1)

    def lookup(self, ip: str) -> Union[IPGeoLocation, Dict[str, str]]:
        """Lookup geolocation information for an IP address"""
        if not self.lookup_city or not self.lookup_country or not self.lookup_asn:
            return {"error": "Databases not loaded"}

        try:
            city_info = self.lookup_city.get(ip)
            country_info = self.lookup_country.get(ip)
            asn_info = self.lookup_asn.get(ip)

            if not city_info and not country_info and not asn_info:
                return {"error": "IP not found"}

            # Extract data safely with fallbacks
            continent = ""
            continent_code = ""
            country = ""
            country_code = ""
            currency = ""

            if country_info:
                continent = country_info.get("continent", {}).get("names", {}).get("en", "")
                continent_code = country_info.get("continent", {}).get("code", "")
                country = country_info.get("country", {}).get("names", {}).get("en", "")
                country_code = country_info.get("country", {}).get("iso_code", "")
                currency = country_info.get("country", {}).get("currency", "")

            # Extract city info
            region = ""
            region_name = ""
            city = ""
            district = ""
            zip_code = ""
            lat = 0.0
            lon = 0.0
            timezone = ""
            offset = 0

            if city_info:
                subdivisions = city_info.get("subdivisions", [])
                if subdivisions:
                    region = subdivisions[0].get("iso_code", "")
                    region_name = subdivisions[0].get("names", {}).get("en", "")
                    if len(subdivisions) > 1:
                        district = subdivisions[1].get("names", {}).get("en", "")

                city = city_info.get("city", {}).get("names", {}).get("en", "")
                zip_code = city_info.get("postal", {}).get("code", "")

                location = city_info.get("location", {})
                lat = location.get("latitude", 0.0)
                lon = location.get("longitude", 0.0)
                timezone = location.get("time_zone", "")
                offset = location.get("accuracy_radius", 0)

            # Extract ASN info
            isp = ""
            org = ""
            as_number = ""
            asname = ""

            if asn_info:
                asn_org = asn_info.get("autonomous_system_organization", "")
                asn_num = asn_info.get("autonomous_system_number", "")

                isp = asn_org
                org = asn_org
                as_number = f"AS{asn_num} {asn_org}"
                asname = asn_org

            # Return Pydantic model instance
            return IPGeoLocation(
                query=ip,
                status="success",
                continent=continent,
                continentCode=continent_code,
                country=country,
                countryCode=country_code,
                region=region,
                regionName=region_name,
                city=city,
                district=district,
                zip=zip_code,
                lat=lat,
                lon=lon,
                timezone=timezone,
                offset=offset,
                currency=currency,
                isp=isp,
                org=org,
                as_=as_number, 
                asname=asname,
            )

        except ValueError:
            return {"error": "Invalid IP address format"}
        except Exception as e:
            logger.error(f"Lookup error for {ip}: {str(e)}")
            return {"error": f"Lookup error: {str(e)}"}


# Create singleton instance
geoip_service = GeoIPService()

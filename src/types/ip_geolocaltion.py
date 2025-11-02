from pydantic import BaseModel, Field

class IPGeoLocation(BaseModel):
    query: str = ""
    status: str = ""
    continent: str = ""
    continentCode: str = ""
    country: str = ""
    countryCode: str = ""
    region: str = ""
    regionName: str = ""
    city: str = ""
    district: str = ""
    zip: str = ""
    lat: float = 0.0
    lon: float = 0.0
    timezone: str = ""
    offset: int = 0
    currency: str = ""
    isp: str = ""
    org: str = ""
    as_: str = Field(default="", alias="as")  # Use alias with default value
    asname: str = ""

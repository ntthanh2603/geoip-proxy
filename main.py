import uvicorn
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "4360"))

    print(f"🚀 GeoIP Server is starting on port {port}...")

    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )

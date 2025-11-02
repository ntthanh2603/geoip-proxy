import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "4360"))

    print(f"🚀 GeoIP Proxy is starting on port {port}...")

    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )

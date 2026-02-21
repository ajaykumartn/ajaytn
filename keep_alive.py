"""
Keep-alive service to prevent Render free tier from sleeping
Pings the application every 14 minutes to keep it active
"""
import requests
import time
import os
from datetime import datetime

# Your Render app URL (update this after deployment)
APP_URL = os.getenv('APP_URL', 'https://your-app-name.onrender.com')
PING_INTERVAL = 840  # 14 minutes (Render sleeps after 15 minutes of inactivity)

def ping_app():
    """Ping the application to keep it alive"""
    try:
        response = requests.get(f"{APP_URL}/health", timeout=10)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if response.status_code == 200:
            print(f"[{timestamp}] ✓ Ping successful - App is alive")
        else:
            print(f"[{timestamp}] ⚠ Ping returned status {response.status_code}")
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✗ Ping failed: {str(e)}")

def main():
    """Main keep-alive loop"""
    print(f"Keep-alive service started for {APP_URL}")
    print(f"Pinging every {PING_INTERVAL} seconds ({PING_INTERVAL/60} minutes)")
    
    while True:
        ping_app()
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()

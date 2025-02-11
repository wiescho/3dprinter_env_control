import asyncio
import aiohttp
import json

# URL of your sensor API
MC_SENSOR_URL = "http://printer_env/sensor"  # Change to your microcontroller’s address
# Moonraker’s HTTP API endpoint (adjust host/port as needed)
MOONRAKER_URL = "http://localhost:7125/printer/gcode/script"

POLL_INTERVAL = 10  # seconds between polls

async def poll_and_update():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(MC_SENSOR_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Assume data is in the form:
                        # { "temperature": 30, "humidity": 45 }
                        temp = data.get("temperature")
                        humid = data.get("humidity")
                        
                        if temp is not None:
                            gcode_temp = f"SET_REMOTE_TEMP sensor=ext_temp temperature={temp}"
                            await session.post(MOONRAKER_URL, json={"script": gcode_temp})
                        if humid is not None:
                            gcode_humid = f"SET_REMOTE_TEMP sensor=ext_humidity temperature={humid}"
                            await session.post(MOONRAKER_URL, json={"script": gcode_humid})
                        print("Updated remote sensors:", temp, humid)
                    else:
                        print("Error: sensor API returned status", response.status)
            except Exception as e:
                print("Error polling sensor:", e)
            await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(poll_and_update())

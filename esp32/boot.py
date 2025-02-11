# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import network
import time
import webrepl
webrepl.start()

# boot.py

SSID = "SSID"
PASSWORD = "PASSWORD"
HOSTNAME = "printer_env"  # hostname i want to use.

def connect_wifi(ssid, password, hostname, timeout=10):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    # Set the DHCP hostname (available on ESP32 MicroPython)
    try:
        wlan.config(dhcp_hostname=hostname)
    except Exception as e:
        print("Could not set DHCP hostname:", e)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi network:", ssid)
        wlan.connect(ssid, password)
        t_start = time.time()
        while not wlan.isconnected():
            if time.time() - t_start > timeout:
                print("Connection timed out!")
                break
            time.sleep(1)
    if wlan.isconnected():
        print("Connected!")
        print("Network configuration:", wlan.ifconfig())
    else:
        print("Failed to connect to Wi-Fi.")
    return wlan

# Attempt to connect with the desired hostname.
wlan = connect_wifi(SSID, PASSWORD, HOSTNAME)



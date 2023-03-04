import digitalio
from time import sleep
import board
import os
import ipaddress
import wifi
import socketpool
import adafruit_requests as requests

#  connect to your SSID
wifi.radio.connect(
    os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
)

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4) * 1000))

# Real LED is on GP16
led = digitalio.DigitalInOut(board.GP16)
# Onboard LED
# led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT

justPressed = False

ntfy_url = "http://ntfy.sh/" + os.getenv("NTFY_ID")
http = requests.Session(pool)


def notify():
    response = http.post(
        ntfy_url,
        data="Go get it ya dumbass",
        headers={
            "Title": "There's someone at the door!",
            "Tags": "bell",
            "Priority": "5",
        },
    )

    json_resp = response.json()
    print(json_resp)


while True:
    if not button.value:
        # Only do once per press
        if not justPressed:
            justPressed = True
            led.value = True
            print("Button down")
            notify()
            # Keep led on for a second
            sleep(1)
            led.value = False

    else:
        justPressed = False

    sleep(0.1)  # debounce delay

import requests
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment



KEY = "f2659bb371647d143bb8f9be29d77eff"
LOCATION = "50.8806289,4.7078858"

def get_current_and_future_temp():
    url = "https://api.darksky.net/forecast/" + KEY + "/" + LOCATION + "?units=si"
    data = requests.get(url).json()
    curr = data["currently"]["temperature"]
    future = data["hourly"]["data"][6]["temperature"]
    return curr, future

def format_temp(temp):
    as_str = str(round(temp)) + "°"
    spaces = " " * (4 - len(as_str))
    return as_str + spaces

def get_segment():
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial)
    return sevensegment(device)

def print_temp(curr, future, segment):
    segment.text = format_temp(curr) + format_temp(future)


if __name__ == "__main__":
    seg = get_segment()
    while True:
        curr, future = get_current_and_future_temp()
        print_temp(curr, future, seg)
        time.sleep(900)

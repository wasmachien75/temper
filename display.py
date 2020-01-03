import requests
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment
from datetime import datetime
import math



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

def print_train(train_tup, segment):
    s = train_tup[0]
    if train_tup[1] > 0:
        s += "[+" + str(train_tup[1]) + "]"
    segment.text = s

def waiting(segment):
    segment.text = "..."

def get_next_trains():
    url = "https://api.irail.be/connections/?from=Leuven&to=Brussels-North&format=json"
    headers = {
        'User-Agent': 'willemvanlishout@gmail.com',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    first_trains = [(x["departure"]["time"], x["departure"]["delay"]) for x in data["connection"][0:3]]
    return [(epoch_to_hhmm(t[0]), math.floor(int(t[1]) / 60) ) for t in first_trains]

def epoch_to_hhmm(epoch):
    ts = datetime.fromtimestamp(int(epoch))
    return ts.strftime("%H%M")


if __name__ == "__main__":
    seg = get_segment()
    while True:
        waiting(seg)
        curr, future = get_current_and_future_temp()
        trains = get_next_trains()
        cnt = 0
        while cnt < 50:
            cnt += 1
            print_temp(curr, future, seg)
            time.sleep(6)
            for train in trains:
                print_train(train, seg)
                time.sleep(6)



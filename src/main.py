import os
import time
import displayio

from src.display import Display, create_text
from src.networking.bay_area_transit_api_client import (
    BayAreaTransitClient,
    TransitAgency,
)
from src.networking.requests import requests

API_KEY = os.getenv("TRANSIT_API_KEY")
STATIONS = os.getenv("PARENT_STATIONS", "").split(",")

UPDATE_DELAY = 120  # s


def initialize_display() -> Display:
    displayio.release_displays()
    display = Display(
        width=64,
        height=64,
        serpentine=True,
        tile_rows=2,
    )

    return display


def main():
    display = initialize_display()
    group = display.add_group()
    text = create_text(
        text="LOADING",
    )
    group.append(text)

    client = BayAreaTransitClient(
        api_key=API_KEY,
        requests=requests,
    )

    last_update = 0
    while True:
        now = time.time()
        if (now - last_update) < UPDATE_DELAY:
            time.sleep(1)
            continue
        last_update = now

        stops = client.get_stops_for_parent_stations(
            agency=TransitAgency.CALTRAIN, parent_stations=STATIONS
        )

        stop_strings = []
        for station, station_stops in stops.items():
            stop_ids = "\n".join([f"  {s["id"]}" for s in station_stops])
            stop_strings.append(f"{station}:\n{stop_ids}")

        group.remove(text)
        text = create_text(text="\n".join(stop_strings))
        group.append(text)

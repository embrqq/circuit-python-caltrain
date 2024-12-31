import os
import time
import displayio
# from src.weather_api import WeatherClient
from src.display import Display, create_text

LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))

displayio.release_displays()
display = Display(
    width=64,
    height=64,
    serpentine=True,
    tile_rows=2,
)
group = display.add_group()
text = create_text(text="hi\nSunny", anchored_position=(5,5))
group.append(text)

while True:
    # forecast = WeatherClient.query_forecast_by_coordinates(
    #     latitude=LATITUDE,
    #     longitude=LONGITUDE,
    # )
    # print(forecast)
    time.sleep(1)

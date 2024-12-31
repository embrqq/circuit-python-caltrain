from .exceptions import HTTPException

WEATHER_API_URL = "https://api.weather.gov"

class WeatherClient:
    """
    Weather Client that hits the national weather service's API.

    It is a light wrapper around the adafruit requests object.
    """

    def __init__(
        self,
        requests,
    ):
        self._requests = requests

    def __make_request(
        self,
        url: str,
    ):
        resp = self._requests.get(url)

        if resp.status_code != 200:
            raise HTTPException(f"Received non-ok status code from {url}: {resp.status_code}")
        
        return resp

    def query_grid(
        self,
        latitude: float,
        longitude: float,
    ) -> tuple:
        """
        Query the National Weather Service to retrieve the grid
        location for the given coordinates

        :returns Tuple[str, int, int]: the grid ID, X, and Y values
        """
        latitude = round(latitude, 4)
        longitude = round(longitude, 4)
        
        url = f"{WEATHER_API_URL}/points/{latitude},{longitude}"
        resp = self.__make_request(url)
        
        json = resp.json()
        properties = json["properties"]
        grid_id = properties["gridId"]
        grid_x = properties["gridX"]
        grid_y = properties["gridY"]

        return (grid_id, grid_x, grid_y)

    def query_forecast(
        self,
        grid_id: str,
        grid_x: int,
        grid_y: int,
        hourly: bool = False
    ) -> dict:
        """
        Queries the weather for a given grid location.

        Returns data as a dict of:
        ```
            {
                "start_time": "YYYY-MM-DDThh:mm:ss-hh:mm",
                "end_time": "YYYY-MM-DDThh:mm:ss-hh:mm",
                "temperature": int,
                "temperature_unit": str,
                "precipitation_probability": int,
                "description": str,
            }
        ```
        """
        url = f"{WEATHER_API_URL}/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast"
        if hourly:
            url = f"{url}/hourly"

        resp = self.__make_request(url)

        json = resp.json()
        periods: list = json["properties"]["periods"]
        now = periods[0]

        return {
            "start_time": now["startTime"],
            "end_time": now["endTime"],
            "temperature": now["temperature"],
            "temperature_unit": now["temperatureUnit"],
            "precipitation_probability": now["probabilityOfPrecipitation"]["value"],
            "description": now["shortForecast"],
        }

    def query_forecast_by_coordinates(
        self,
        latitude: int,
        longitude: int,
        hourly: bool = False,
    ):
        
        grid_id, grid_x, grid_y = self.query_grid(
            latitude=latitude,
            longitude=longitude,
        )
        forecast = self.query_forecast(
            grid_id=grid_id, 
            grid_x=grid_x, 
            grid_y=grid_y, 
            hourly=hourly,
        )
        return forecast

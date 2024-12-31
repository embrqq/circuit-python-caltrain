import os
from enum import Enum
from .exceptions import HTTPException

TRANSIT_API_HOST = "http://api.511.org"

class TransitAgency(str, Enum):
    """
    Enum for transit agencies in the bay area.

    The values for this enum can be found by querying:
    `http://api.511.org/transit/gtfsoperators?api_key=[your_key]`
    """

    TRI_DELTA_TRANSIT = "3D"
    AC_TRANSIT = "AC"
    ANGEL_ISLAND_TIBURON_FERRY = "AF"
    CAPITOL_CORRIDOR_JOINT_POWERS_AUTHORITY = "AM"
    BAY_AREA_RAPID_TRANSIT = "BA"
    COUNTY_CONNECTION = "CC"
    ALTAMONT_CORRIDOR_EXPRESS = "CE"
    COMMUTE_ORG_SHUTTLES = "CM"
    CALTRAIN = "CT"
    DUMBARTON_EXPRESS_CONSORTIUM = "DE"
    EMERY_GO_ROUND = "EM"
    FAST = "FS"
    GOLDEN_GATE_FERRY = "GF"
    GOLDEN_GATE_TRANSIT = "GG"
    MARIN_TRANSIT = "MA"
    MISSION_BAY_TMA = "MB"
    MOUNTAIN_VIEW_COMMUNITY_SHUTTLE = "MC"
    MVGO = "MV"
    PETALUMA = "PE"
    PRESIDIO_GO = "PG"
    REGIONAL_GTFS = "RG"
    RIO_VISTA_DELTA_BREEZE = "RV"
    SONOMA_MARIN_AREA_RAIL_TRANSIT = "SA"
    SAN_FRANCISCO_BAY_FERRY = "SB"
    VTA = "SC"
    SAN_FRANCISCO_MUNICIPAL_TRANSPORTATION_AGENCY = "SF"
    SAN_FRANCISCO_INTERNATIONAL_AIRPORT = "SI"
    SAMTRANS = "SM"
    SONOMA_COUNTY_TRANSIT = "SO"
    SANTAROSA = "SR"
    CITY_OF_SOUTH_SAN_FRANCISCO = "SS"
    SOLTRANS = "ST"
    TREASURE_ISLAND_FERRY = "TF"
    UNION_CITY_TRANSIT = "UC"
    VACAVILLE_CITY_COACH = "VC"
    VINE_TRANSIT = "VN"
    WESTERN_CONTRA_COSTA = "WC"
    LIVERMORE_AMADOR_VALLEY_TRANSIT_AUTHORITY = "WH"


class BayAreaTransitClient:
    """
    A client that provides an interface for fetching train data
    from 511.org
    """

    def __init__(
        self,
        api_key: str,
        requests,
    ):
        """
        Initialize a client to query 511.org for bay area transit data.

        :param str api_key: API key received on account creation from 511.org
        :param requests: the requests object to use, specified to allow for
        testing of the client with the standard Python requests library instead
        of the CircuitPython library.
        """
        self._api_key = api_key
        self._requests = requests

    def __make_request(
        self,
        url: str,
        params: dict | None = None,
    ):
        resp = self._requests.get(url, params=params)

        if resp.status_code != 200:
            raise HTTPException(f"Received non-ok status code from {url}: {resp.status_code}")
        
        return resp

    def get_real_time_arrival_departures(
        self,
        agency: TransitAgency,
        stopcode: str | None = None,
    ):
        url = f"{TRANSIT_API_HOST}/transit/StopMonitoring"
        params = {
            "api_key": self._api_key,
            "agency": agency.value,
            "format": "JSON",
        }

        resp = self.__make_request(url=url, params=params)

    def get_stops_for_agency(
        self,
        agency: TransitAgency,
    ) -> list:
        """
        Fetches all stop for the given transit agency, returning a list
        of dicts of each stop.

        :param TransitAgency agency: the agency to fetch stops for
        """
        url = f"{TRANSIT_API_HOST}/transit/stops"
        params = {
            "api_key": self._api_key,
            "agency": agency.value,
            "format": "JSON",
        }

        resp = self.__make_request(url=url, params=params)

        return resp["Contents"]["dataObjects"]["ScheduledStopPoint"]

    def get_stops_for_parent_stations(
        self,
        agency: TransitAgency,
        parent_stations: list,
    ) -> dict:
        """
        Gets all the stop IDs associated with the parent station
        at the given agency.

        Returns data as a dict of lists like:
        ```json
        {
            "menlo_park": [
                {
                    "agency": TransitAgency,
                    "id": 70161,
                    "name": "Menlo Park Caltrain Station Northbound",
                    "parent_station": "menlo_park",
                    "longitude": -122.182297,
                    "latitude": 37.454856,
                }
            ]
        }
        ```

        :param TransitAgency agency: the agency to fetch stops for
        :param List[str] parent_station: the list of parent stations to
        fetch stops for
        :return List[dict]: the list of stops for the given parent stations
        """

        stops = self.get_stops_for_agency(agency)

        return_values = {ps: [] for ps in parent_stations}
        for stop in stops:
            ps = stop["Extensions"].get("ParentStations")
            if not ps in parent_stations:
                continue

            return_values[ps].append({
                "agency": agency,
                "id": stop["id"],
                "name": stop["Name"],
                "parent_station": ps,
                "longitude": float(stop["Location"]["Longitude"]),
                "latitude": float(stop["Location"]["Latitude"]),
            })
        
        return return_values
import requests
from src.networking.bay_area_transit_api_client import (
    TransitAgency,
    BayAreaTransitClient,
)


def test_get_stops_for_menlo_park(
    api_key,
):
    client = BayAreaTransitClient(
        api_key=api_key,
        requests=requests,
    )

    resp = client.get_stops_for_parent_stations(
        agency=TransitAgency.CALTRAIN,
        parent_stations=["menlo_park"],
    )

    assert "menlo_park" in resp
    stations = resp["menlo_park"]
    stations = sorted(stations, key=lambda row: row["id"])
    assert stations == [
        {
            "agency": TransitAgency.CALTRAIN,
            "id": 70161,
            "name": "Menlo Park Caltrain Station Northbound",
            "longitude": -122.182297,
            "latitude": 37.454856,
        },
        {
            "agency": TransitAgency.CALTRAIN,
            "id": 70162,
            "name": "Menlo Park Caltrain Station Southbound",
            "longitude": -122.182405,
            "latitude": 37.454745,
        },
    ]

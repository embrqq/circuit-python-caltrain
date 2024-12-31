import pytest
import toml


@pytest.fixture(scope="session")
def api_key():
    with open("./settings.toml", "r") as file:
        settings = toml.load(file)
    api_key = settings.get("TRANSIT_API_KEY")
    if api_key is None:
        raise Exception("TRANSIT_API_KEY variable not set in 'settings.toml'.")

    return api_key

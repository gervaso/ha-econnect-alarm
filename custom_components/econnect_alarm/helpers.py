"""Helper methods to reuse common logic across econnect_alarm module."""
from elmo.api.client import ElmoClient
from homeassistant import core
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from .const import CONF_DOMAIN, CONF_SYSTEM_URL
from .exceptions import InvalidAreas


def parse_areas_config(config: str, raises: bool = False):
    """Parses a comma-separated string of area configurations into a list of integers.

    Takes a string containing comma-separated area IDs and converts it to a list of integers.
    In case of any parsing errors, either raises a custom `InvalidAreas` exception or returns an empty list
    based on the `raises` flag.

    Args:
        config (str): A comma-separated string of area IDs, e.g., "3,4".
        raises (bool, optional): Determines the error handling behavior. If `True`, the function
                                 raises the `InvalidAreas` exception upon encountering a parsing error.
                                 If `False`, it suppresses the error and returns an empty list.
                                 Defaults to `False`.

    Returns:
        list[int]: A list of integers representing area IDs. If parsing fails and `raises` is `False`,
                   returns an empty list.

    Raises:
        InvalidAreas: If there's a parsing error and the `raises` flag is set to `True`.

    Examples:
        >>> parse_areas_config("3,4")
        [3, 4]
        >>> parse_areas_config("3,a")
        []
    """
    if config == "" or config is None:
        # Empty config is considered valid (no sectors configured)
        return []

    try:
        return [int(x) for x in config.split(",")]
    except (ValueError, AttributeError):
        if raises:
            raise InvalidAreas
        return []


async def validate_credentials(hass: core.HomeAssistant, config: dict):
    """Validate if user input includes valid credentials to connect.

    Initialize the client with an API endpoint and a vendor and authenticate
    your connection to retrieve the access token.

    Args:
        hass: HomeAssistant instance.
        data: data that needs validation (configured username/password).
    Raises:
        ConnectionError: if there is a connection error.
        CredentialError: if given credentials are incorrect.
        HTTPError: if the API backend answers with errors.
    Returns:
        `True` if given `data` includes valid credential checked with
        e-connect backend.
    """
    # Check Credentials
    client = ElmoClient(config.get(CONF_SYSTEM_URL), domain=config.get(CONF_DOMAIN))
    await hass.async_add_executor_job(client.auth, config.get(CONF_USERNAME), config.get(CONF_PASSWORD))
    return True

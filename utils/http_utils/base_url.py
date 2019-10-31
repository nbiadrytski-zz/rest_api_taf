from tests.data.constants import (
    BASE_HOST,
    BASE_PATH
)


class BaseUrl:
    """Builds base_url based on provided request host and path."""

    def __init__(self, host=BASE_HOST, path=BASE_PATH):
        """
        Initialise base_url composed from host and path.

        :param host: endpoint host
        :param path: endpoint path
        """
        self.host = host
        self.path = path
        self.base_url = self.host + self.path

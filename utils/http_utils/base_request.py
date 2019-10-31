from abc import (
    ABCMeta,
    abstractmethod
)


class BaseRequest(metaclass=ABCMeta):
    """Provides abstract call() method to be implemented by child request classes."""

    @abstractmethod
    def call(self, *args, **kwargs):
        """Obligatory method for each HTTP request class."""
        raise NotImplementedError

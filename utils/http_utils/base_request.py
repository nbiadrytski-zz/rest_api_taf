from abc import (
    ABCMeta,
    abstractmethod
)


class BaseRequest(metaclass=ABCMeta):
    """
    Provides abstract method call() to be implemented by child classes.
    """

    @abstractmethod
    def call(self, *args, **kwargs):
        """
        Obligatory method for each HTTP request.

        :param args:
        :param kwargs:
        """
        raise NotImplementedError

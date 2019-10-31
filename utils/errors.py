class Error(Exception):
    """Base custom errors class."""

    def __str__(self):
        """
        Return error message string representation.

        :return: <str> error message
        """
        return f'{self.message}'


class UnsupportedEnvException(Error):
    """Raised if invalid --env value or no value is passed as command line arg."""

    def __init__(self, env, supported_envs):
        """
        Initialise UnsupportedEnvException.

        :param env: <str> environment
        :param supported_envs: supported environments
        """
        self.message = f'\n"{env}" is not a supported environment.\n' \
            f'Supported environments: {supported_envs}.'


class NoEnvArgException(Error):
    """Raised if --env command line arg was not passed when starting tests."""

    def __init__(self, env):
        """
        Initialise NoEnvArgException.

        :param env: <str> environment
        """
        self.message = f'\nCommand line arg "--env" is missing. Env is {env}.'

import configparser


class DataConfigParser:
    """
    Parses data from config .ini files.

    Parameters:
        config_path (str): relative path to config file.
    """
    def __init__(self, config_path):
        """
        Initialise DataConfigParser.

        :param config_path:<str> path to config
        """
        self.parser = configparser.ConfigParser()
        self.parser.read(config_path)

    def get_supported_envs(self, section):
        """
        Get dict of supported environments.

        :param section:<str> title of config section
        :return: dict of supported environments
        """
        return dict(self.parser.items(section))

    def get_value(self, section, key):
        """
        Get config value by passed section title and its key.

        :param section:<str> title of config section
        :param key:<str> title of section key
        :return: <str> key value
        """
        return self.parser.get(section, key)

    def get_ignored_keys(self, title, keys):
        """
        Get config key values to be ignored.
        Based on provided config section title and keys.

        :param title: title of config section
        :param keys: keys to be ignored
        :return: tuple of ignored keys
        """
        ignored_keys = []
        for key in keys:
            key = self.parser.get(title, key)
            ignored_keys.append(key)
        return tuple(ignored_keys)

import os
import json
import logging

import dictdiffer
from jsonpath_rw import parse as json_parser

from utils.config_parser import DataConfigParser
from utils.errors import UnsupportedEnvException
from utils.constants import (
    ENVS_CONFIG_PATH,
    JSON_KEYS_CONFIG_PATH
)


LOGGER = logging.getLogger(__name__)


def get_host(env):
    """
    Returns supported host value (e.g. http://127.0.0.1:5000) by parsing envs_config.ini.
    If env is not in envs_config.ini, then custom UnsupportedEnvException is raised.

    :param env: <str> environment key, e.g. 'dev'
    :return: host: <str> host string, e.g. 'http://127.0.0.1:5000'
    """
    cfg = DataConfigParser(ENVS_CONFIG_PATH)
    supported_envs = cfg.get_supported_envs(section='envs')
    if env.lower() not in supported_envs:
        raise UnsupportedEnvException(env, supported_envs)
    host = supported_envs[env.lower()]
    return host


def find_item_by_jsonpath(actual_json, json_path, idx=0):
    """
    Get JSON key value by json_path using jsonpath_rw module.
    Default idx=0 to get the 1st item from resulting list.

    :param actual_json: <dict> json response
    :param json_path: <str> path to key
    :param idx: <int> first item from resulting list
    :return: value: <str> key value
    """
    return [match.value for match in json_parser(json_path).find(actual_json)][idx]


def file_content(file_path):
    """
    Return file content based on provided file path.

    :param file_path: <str> relative path to file
    :return: <str> file content
    """
    file_ = os.path.join(os.getcwd(), file_path)
    if os.path.isfile(file_):
        with open(file_) as f:
            return f.read()
    else:
        LOGGER.error('File %s was not found', file_)
        raise FileNotFoundError


def convert_json_to_dict(file_path):
    """
    Convert .json file content to dictionary.

    :param file_path: <str> relative path to .json file
    :return: dictionary
    """
    file_ = os.path.join(os.getcwd(), file_path)
    if os.path.isfile(file_):
        with open(file_) as f:
            return json.load(f)
    else:
        LOGGER.error('File %s was not found', file_)
        raise FileNotFoundError


def compare_dicts(actual_dict, expected_dict, ignore_keys):
    """
    Compare 2 dicts are equal using dictdiffer module, loggs diff.
    Pass the keys to be ignored to ignore_keys param.

    :param actual_dict: <dict> actual dictionary
    :param expected_dict: <dict> expected dictionary
    :param ignore_keys: <tuple> json keys to be ignored
    :return: <bool>: if two dicts are equal
    """
    difference = list(dictdiffer.diff(actual_dict, expected_dict, ignore=ignore_keys))
    if difference:
        LOGGER.error('Responses do not match:\n %s', difference)
        return False
    return True


def case_body(suite_id, title, description):
    """
    Provide dict constant for test case request body.

    :param suite_id: <str> suite id
    :param title: <str> test case title
    :param description:  <str> test case description
    :return: dict for test case request body
    """
    return {"suite_id": suite_id,
            "title": title,
            "description": description}


def get_from_json_path_config(key):
    """
    Get value of the passed key from json_keys_config.ini.

    :param key: key of the desired value
    :return: value:<str>
    """
    return DataConfigParser(JSON_KEYS_CONFIG_PATH).get_value(section='keys', key=key)

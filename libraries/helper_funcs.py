"""Contains keywords used in tests."""

from jsonpath_rw import parse as json_parser


def find_item_by_json_path(actual_json, json_path, idx=0):
    """
    Get JSON key value by passed json_path using jsonpath_rw module.
    Default idx=0 to get the 1st item from resulting list.

    :param actual_json: <dict> actual json response
    :param json_path:   <str> json_path to key
    :param idx:         <int> first item from resulting list
    :return:            key value
    """
    value = [match.value for match in json_parser(
        json_path).find(actual_json)][idx]
    return value


def case_body(suite_id, title, description):
    """
    Provide dict constant for test case request body.

    :param suite_id:     <str> suite id
    :param title:        <str> test case title
    :param description:  <str> test case description
    :return:             dict for test case request body
    """
    return {"suite_id": suite_id,
            "title": title,
            "description": description}


def get_json_key_value(resp, key):
    """
    Gets JSON response key value.

    :param resp: Response object returned by HTTP request
    :param key:  <str>, json response key
    :return:     key value
    """
    actual_json = resp.json()
    value = find_item_by_json_path(actual_json, key)
    return value


def request_headers(header_dict, token):
    """
    Merge request header dict from argument with Authorization header.

    :param header_dict: header dict to be merged with Authorization header
    :param token:       access_token value
    :return:            request headers merged dict
    """
    final_dict = {**header_dict, **{"Authorization": "Bearer " + token}}
    return final_dict

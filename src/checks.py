"""
checks.py
---------
This file contains functions that are solely used to ensure that valid values are passed into functions. This avoids
repeat code and keeps functions.py reserved for functional code only.
"""

import json
import os.path
from json import JSONDecodeError
from typing import TextIO

def has_attr(checkObj: object,
             neededAttr: str) -> None:
    """
    Raises an error if the object does not have an attribute with name neededAttr.

    :param checkObj: The object whose attributes to search.
    :param neededAttr: The attribute name to look for.
    :return: None.
    """
    if not hasattr(checkObj, neededAttr):
        raise AttributeError(f"{checkObj.__class__.__name__} has no attribute '{neededAttr}'")

def is_instance(checkObj: object,
                neededType: type) -> None:
    """
    Raises an error if the object is not an instance of a required type.
    :param checkObj: The object to check.
    :param neededType: The type to look for.
    :return: None.
    """

    if not isinstance(checkObj, neededType):
        raise TypeError(f"{checkObj.__class__.__name__} must be of type {neededType.__name__}")

def validate_json(json_file: TextIO) -> None:
    """
    Determines if a file contains valid JSON.
    :param json_file: The JSON file to validate.
    :return: None.
    """
    try:
        json.load(json_file)
        json_file.seek(0)
    except JSONDecodeError as e:
        file_name = getattr(json_file, "name", "Unknown File")
        raise JSONDecodeError(f"{file_name} is not a valid JSON file", e.doc, e.pos)

def path_exists(path: str) -> None:
    """
    Raises an error if the given path does not exist.
    :param path: A string representing the path to the file/directory.
    :return: None.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot find file/directory in path {path}")
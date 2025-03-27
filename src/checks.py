"""
checks.py
---------
This file contains functions that are solely used to ensure that valid values are passed into functions. This avoids
repeat code and keeps functions.py reserved for functional code only. It also contains functions to simplify
exception raising.
"""

# Import modules
from collections.abc import Sequence
import json
import logging
from math import isfinite
from numbers import Real, Integral
import pygame
from typing import Any, Optional, TextIO

# Initialize modules
logger: logging.Logger = logging.getLogger(__name__)

def only_contains_type(sequence: Sequence,
                  kind: type) -> bool:
    """
    Checks if a sequence only contains a certain type.

    Args:
        sequence (Sequence): The sequence to check.
        kind (Type): The type to look for.

    Returns:
        bool: True if the sequence only contains the given type and is not empty. Otherwise, False.

    Raises:
        TypeError: If sequence is not a sequence.
        warning: If the sequence is empty. Returns False.

    Examples:
        >>> only_contains_type([1, 6 -43], int)
        True
        >>> only_contains_type(["abc", "123", "xyz"], str)
        True
        >>> only_contains_type(["abc", 123, True], str)
        False
    """

    if not is_sequence(sequence):
        raise TypeError(f"A sequence is required. Given type: {sequence.__class__.__name__}")
    if not sequence:
        logger.warning("Attempted to check an empty sequence")
        return False
    if not isinstance(kind, type):
        raise TypeError(f"kind must be a type. Given type: {type(kind)}")

    for item in sequence:
        if type(item) is not kind:
            return False

    return True

def is_boolean(value: Any) -> bool:
    """
    Determines if the given value is a boolean.

    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is a boolean, otherwise False.

    Examples:
        >>> is_boolean(True)
        True
        >>> is_boolean(1)
        False
        >>> is_boolean("abc")
        False
    """

    return type(value) is bool

def is_integer(value: Any) -> bool:
    """
    Determines if a number is an integer or not.

    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is an integer (and not a boolean). Otherwise, False.

    Examples:
        >>> is_integer(1)
        True
        >>> is_integer(3.14)
        False
        >>> is_integer(True)
        False
        >>> is_integer("1")
        False
    """

    return isinstance(value, Integral) and not isinstance(value, bool)

def is_real_number(value: Any) -> bool:
    """
    Determines if the given value is a real number (excluding booleans and non-finite numbers).

    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is a real number and not a boolean or infinity, False otherwise.

    Examples:
        >>> is_real_number(3.14)
        True
        >>> is_real_number(1)
        True
        >>> is_real_number(True)
        False
        >>> is_real_number(float("inf"))
        False
    """

    return isinstance(value, Real) and not isinstance(value, bool) and isfinite(value)

def is_positive(value: Real,
                zero_is_positive: bool = False) -> bool:
    """
    Determines if a number is positive. You can set whether to include zero or not. "nan" and "inf" are not included.
    Booleans are not included.

    Args:
        value (Real): The value to check.
        zero_is_positive (bool): If True, zero is considered positive. False by default.

    Returns:
        bool: True if the value is positive (or zero when zero_is_positive is True), otherwise False.

    Raises:
        ValueError: If the value argument is not a number, including booleans and infinities.

    Examples:
        >>> is_positive(1)
        True
        >>> is_positive(-2)
        False
        >>> is_positive("1")
        ValueError
    """

    if not is_real_number(value):
        raise ValueError(f"is_positive() requires a finite real number value (not including booleans or infinity). "
                         f"Value given: {value}")

    return value >= 0 if zero_is_positive else value > 0

def is_sequence(value: Any,
                size: Optional[int] = None) -> bool:
    """
    Determines if a value is a sequence. If size is set, the sequence must be of that size to return True.

    Args:
        value (Any): The value to check.
        size (Optional[int]): The required size of the sequence. If none is given, any size is acceptable.

    Returns:
        bool: True if the value is a sequence of the given size. Otherwise, False.

    Raises:
        ValueError: If size is not a positive integer.
        TypeError: If size is not an integer.

    Examples:
        >>> is_sequence([1, 2, 3])
        True
        >>> is_sequence((1, 2), 2)
        True
        >>> is_sequence([1, 2], 3)
        False
        >>> is_sequence("abc")
        False
        >>> is_sequence([1, 2], -1)
        ValueError
    """

    # Ensures that size is a positive integer if it is given.
    if size is not None:
        if not isinstance(size, int):
            raise TypeError(f"Size argument must be an integer. Given type: {type(size)}")
        if not is_positive(size):
            raise ValueError(f"Size argument must be positive. Given value: {size}")

    # Returns False if value is not a sequence. Otherwise, if size is given, returns length
    if not isinstance(value, Sequence):
        return False
    if size is not None:
        return len(value) == size
    return True

def is_valid_pygame_color(value: Any) -> bool:
    """
    Determines if a given value will work with PyGame's Color() class.

    Args:
        value (Any): The value to check.

    Returns:
        bool: True if the value is a valid PyGame color, False otherwise.

    Examples:
        >>> is_valid_pygame_color('red')
        True
        >>> is_valid_pygame_color((255, 255, 255))
        True
        >>> is_valid_pygame_color("not-a-color")
        False
    """

    # Attempt to create a color from the given value. If no error is raised, True is returned. Otherwise, False.
    try:
        pygame.Color(value)
        return True
    except (ValueError, TypeError):
        return False

def has_duplicate_values(sequence: Sequence[Any]) -> bool:
    """
    Determines if a sequence has duplicate values.

    Args:
        sequence (Sequence): The sequence to be checked.

    Returns:
        bool: True if there are duplicate values, False otherwise.

    Raises:
        TypeError: If the value passed is not a sequence.
        warning: If the sequence is empty. Returns False
    """

    if not isinstance(sequence, Sequence):
        raise TypeError(f"Requires a sequence type. Given type: {sequence.__class__.__name__}")
    if not sequence:
        logger.warning("Attempted to search for duplicates in an empty sequence.")
        return False

    seen = set()

    for item in sequence:
        if item in seen:
            return True
        seen.add(item)

    return False

def validate_json(json_file: TextIO) -> None:
    """
    Determines if a file contains valid JSON.
    :param json_file: The JSON file to validate.
    :return: None.
    """
    try:
        json.load(json_file)

        # Resets the entry point of the file.
        json_file.seek(0)
    except json.JSONDecodeError as e:
        file_name: str = getattr(json_file, "name", "Unknown File")
        raise json.JSONDecodeError(f"{file_name} is not a valid JSON file", e.doc, e.pos)

def hasinstance(obj: object,
                 kind: type) -> bool:
    """
    Like isinstance, but also checks the object's attributes. Does not check the attributes of attributes.

    Args:
        obj (object): The object to check.
        kind (type): The type to look for.

    Returns:
        bool: True if the object is the given type or has one in its attributes. Otherwise, False.
        warning: If the object has no attributes.

    Raises:
        TypeError: If kind is not a type.

    Examples:
        >>> hasinstance(pygame.sprite.Sprite(), pygame.Mask)
        True
        >>> hasinstance(pygame.Rect(), pygame.Rect)
        True
    """

    if not isinstance(kind, type):
        raise TypeError(f"Kind argument must be a type. Type given: {kind.__class__.__name__}")

    if isinstance(obj, kind):
        return True
    if hasattr(obj, '__dict__'):
        for attr in obj.__dict__.values():
            if isinstance(attr, kind):
                return True
    else:
        logger.warning(f"Object {obj.__class__.__name__} has no attributes.")

    return False
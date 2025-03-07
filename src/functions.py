"""
functions.py
------------
This file holds all the independent helper functions used within the program logic
"""
from checks import has_attr, path_exists, validate_json
import json
import logging
from pathlib import Path
import pygame
from typing import Any, Tuple

current_dir = Path(__file__).resolve().parent
logger = logging.getLogger(__name__)

def get_display_size() -> Tuple[int, int]:
    """
    Returns the size of the current display (in pixels).
    :return: Display size in pixels -> tuple (width, height).
    """

    if not pygame.display.get_init():
        logger.warning("PyGame display module is not initialized")
        logger.info("Initializing display...")

        pygame.display.init()

    display_info = pygame.display.Info()
    size = display_info.current_w, display_info.current_h

    return size

def load_settings(name: str) -> dict[str, Any]:
    """
    Loads a JSON file from the Settings with the name {name}.json and returns the settings as a Python
    dictionary.
    :param name: Name of the JSON file (without '.json').
    :return: Dictionary matching setting names and values.
    """
    logger.debug(f"Settings being loaded for {name}.json")

    path = current_dir / "Settings" / f"{name}.json"
    path_exists(str(path))

    with path.open("r", encoding="utf-8") as file:
        validate_json(file)

        settings = json.load(file)

    logger.debug(f"Settings for {name}: {settings}")
    logger.info(f"Settings loaded for {name}")

    return settings

def load_controls(controls: dict[str, str]) -> dict[str, int]:
    """
    Converts a dictionary of action names, key names to action names, PyGame key constants.
    :param controls: Dictionary mapping action names to key names.
    :return: Dictionary mapping action names to PyGame key constants.
    """
    pygame_dict: dict[str, int] = {}

    for action, key in controls.items():
        # PyGame key constants are lowercase if it is a letter and uppercase if it is a word, like escape or return
        if len(key) == 1:
            key_name = f"K_{key.lower()}"
        else:
            key_name = f"K_{key.upper()}"

        has_attr(pygame, key_name)
        pygame_key = getattr(pygame, key_name)

        pygame_dict[action] = pygame_key

    return pygame_dict
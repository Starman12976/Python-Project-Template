"""
functions.py
------------
This file holds all the independent helper functions used within the program logic
"""

from checks import (is_boolean, is_integer, is_positive, is_real_number, has_duplicate_values, only_contains_type,
                    validate_json, is_sequence, hasinstance)
import json
import logging
from numbers import Real
import os
from pathlib import Path
import pygame
from typing import Any, Dict, List, Optional, Tuple

current_dir: Path = Path(__file__).resolve().parent
logger: logging.Logger = logging.getLogger(__name__)

def get_display_size() -> Tuple[int, int]:
    """
    Returns the size of the current display (in pixels).

    Returns:
        Tuple[int, int]: Tuple representing screen width and height.

    Raises:
        warning: If the display module is not initialized. It will initialize it for you.
    """

    # Ensure display is initialized
    if not pygame.display.get_init():
        logger.warning("PyGame display module is not initialized")
        logger.info("Initializing display...")

        pygame.display.init()

    display_info: pygame.display.Info = pygame.display.Info()
    size: tuple[int, int] = display_info.current_w, display_info.current_h

    return size

def load_controls(controls: Dict[str, str]) -> Dict[str, int]:
    """
    Converts a dictionary of action names, key names to action names, PyGame key constants.

    Args:
        controls (Dict[str, str]): Dictionary mapping action names to key names.

    Returns:
        Dict[str, int]: Dictionary mapping action names to PyGame key constants.
    """
    pygame_dict: Dict[str, int] = {}

    for action, key in controls.items():
        # PyGame key constants are lowercase if it is a letter and uppercase if it is a word, like escape or return
        if len(key) == 1:
            key_name: str = f"K_{key.lower()}"
        else:
            key_name: str = f"K_{key.upper()}"

        # Ensure that the key name is valid.
        if not hasattr(pygame, key_name):
            raise ValueError(f"Invalid key name. Name given: pygame.K_{key_name}")
        else:
            pygame_key: int = getattr(pygame, key_name)
            pygame_dict[action] = pygame_key

    return pygame_dict

def load_settings(name: str) -> Dict[str, Any]:
    """
    Loads a JSON file from the Settings with the name {name}.json and returns the settings as a Python
    dictionary.

    Args:
        name (str): Name of the json file. Do not include '.json'.

    Returns:
        Dict[str, Any]: Dictionary matching setting names and values.

    Raises:
        FileNotFoundError: If the JSON file does not exist in src/Settings.
        JSONDecodeError: If the JSON file is formatted incorrectly.
    """
    logger.debug(f"Settings being loaded for {name}.json")

    path: Path = current_dir / "Settings" / f"{name}.json"

    if not os.path.exists(str(path)):
        raise FileNotFoundError(f"JSON does not exist. Path given: {path}")

    with path.open("r", encoding="utf-8") as file:
        validate_json(file)

        settings: Dict[str, Any] = json.load(file)

    logger.debug(f"Settings for {name}: {settings}")
    logger.info(f"Settings loaded for {name}")

    return settings

def load_sprite_sheet(sheet: pygame.Surface,
                        sprite_width: int,
                        sprite_height: int,
                        sprite_names: List[str]) -> Dict[str, List[pygame.Surface]]:
    """
    Splits a single sprite sheet into a dictionary mapping sprite names to a list containing frames of the animation.
    Each row of sprites corresponds to the matching index in sprite_names. For example, row 1 will be matched with
    sprite_names[0], row 2 will be matched with sprite_names[1], etc.

    Args:
        sheet (pygame.Surface): Sprite sheet image as a PyGame Surface.
        sprite_width (int): Width of each sprite.
        sprite_height (int): Height of each sprite.
        sprite_names (List[str]): List of sprite names. The index corresponds to the rows in the sprite sheet.

    Returns:
        A dictionary matching sprite names with a list of individual sprites making up the animation.

    Raises:
        TypeError: If sheet is not a surface, width/height are not integers, or sprite_names is not a sequence of strings.
        ValueError: If width/height are not positive or sprite names are duplicated.
    """

    if not isinstance(sheet, pygame.Surface):
        raise TypeError(f"Sprite sheet must be a Surface. Type given: {sheet.__class__.__name__}")
    if not is_sequence(sprite_names):
        raise TypeError(f"Sprite names must be a sequence. Type given: {sprite_names.__class__.__name__}")
    if has_duplicate_values(sprite_names):
        raise ValueError("Sprite names cannot contain duplicate values.")
    if not only_contains_type(sprite_names, str):
        raise ValueError("Sprite names must be a sequence of only strings.")
    if not is_integer(sprite_width):
        raise TypeError(f"Sprite width must be an integer. Type given: {sprite_width.__class__.__name__}")
    if not is_positive(sprite_width):
        raise ValueError("Sprite width must be positive.")
    if not is_integer(sprite_height):
        raise TypeError(f"Sprite height must be an integer. Type given: {sprite_width.__class__.__name__}")
    if not is_positive(sprite_height):
        raise ValueError("Sprite height must be positive.")

    sheet_width: int = sheet.get_width()
    sheet_height: int = sheet.get_height()

    if sheet_width % sprite_width != 0:
        raise ValueError(f"Sheet width must be divisible by sprite width. "
                         f"Sprite width: {sprite_width}, sheet width: {sheet_width}")
    if sheet_height % sprite_height != 0:
        raise ValueError(f"Sheet height must be divisible by sprite height. "
                         f"Sprite height: {sprite_height}, sheet height: {sheet_height}")

    num_animations: int = sheet_height // sprite_height
    num_sprites: int = sheet_width // sprite_width

    if len(sprite_names) != num_animations:
        raise ValueError(f"The number of animations, {num_animations}, must match the number "
                         f"of animation names, {len(sprite_names)}")

    sprite_dict: Dict[str, List[pygame.Surface]] = {}

    for animation_index in range(num_animations):
        current_animation: str = sprite_names[animation_index]
        sprite_dict[current_animation] = []

        y_offset: int = animation_index * sprite_height

        for sprite_index in range(num_sprites):
            x_offset: int = sprite_index * sprite_width

            rect: pygame.Rect = pygame.Rect(x_offset, y_offset, sprite_width, sprite_height)
            sprite: pygame.Surface = sheet.subsurface(rect).copy()

            sprite_dict[current_animation].append(sprite)

    return sprite_dict

def scale_image(image: pygame.Surface,
                scale: Real,
                is_smooth: bool = False) -> pygame.Surface:
    """
    Scales an image with a give scale.

    Args:
        image (pygame.Surface): The image to resize.
        scale (Real): The scale to resize to. Must be a positive real number.
        is_smooth (bool): Uses bilinear scaling. Off by default.

    Returns:
        pygame.Surface: The rescaled image. If scale is 1, it returns the original image.

    Raises:
        ValueError: If scale is not a positive number
        TypeError: If image is not a surface, scale is not a number, or is_smooth is not a boolean.
    """

    if not isinstance(image, pygame.Surface):
        raise TypeError(f"Image must be a Surface. Given type: {image.__class__.__name__}")
    if not is_real_number(scale):
        raise TypeError(f"Scale must be a number. Given type: {scale.__class__.__name__}")
    if not is_positive(scale):
        raise ValueError(f"Scale must be a positive number. Given value: {scale}")
    if not is_boolean(is_smooth):
        raise TypeError(f"is_smooth must be a boolean. Given value: {is_smooth}")

    if scale == 1:
        return image

    image_width: int = image.get_width()
    image_height: int = image.get_height()

    new_width: int = int(image_width * scale)
    new_height: int = int(image_height * scale)
    new_size: [int, int] = (new_width, new_height)

    if new_width < 1 or new_height < 1:
        raise ValueError("Scaling results in zero or negative dimensions.")

    if is_smooth:
        scaled_image: pygame.Surface = pygame.transform.smoothscale(image, new_size)
    else:
        scaled_image: pygame.Surface = pygame.transform.scale(image, new_size)

    logger.debug(f"Image scaled from ({image_width}, {image_height}) to ({new_width}, {new_height}). "
                 f"Smooth={is_smooth}")

    return scaled_image

def get_collision(obj1: object,
                  obj2: object) -> tuple[int, int] | None:
    """
    Returns the collision point between two objects, if any. Requires the objects to have rects and masks.

    Args:
        obj1 [object]: The first object.
        obj2 [object]: The second object.

    Returns:
        tuple[int, int] | None: A tuple representing the collision point. If no collision, None is returned.

    Raises:
        AttributeError: Obj1/2 does not have a rect or mask in its attributes.
    """

    if not hasinstance(obj1, pygame.Rect):
        raise AttributeError(f"Object 1 must have a rect.")
    if not hasinstance(obj1, pygame.Mask):
        raise AttributeError(f"Object 1 must have a mask.")
    if not hasinstance(obj2, pygame.Rect):
        raise AttributeError(f"Object 2 must have a rect.")
    if not hasinstance(obj2, pygame.Mask):
        raise AttributeError(f"Object 2 must have a mask.")

    rect1: pygame.Rect = getinstance(obj1, pygame.Rect)
    rect2: pygame.Rect = getinstance(obj2, pygame.Rect)
    mask1: pygame.Mask = getinstance(obj1, pygame.Mask)
    mask2: pygame.Mask = getinstance(obj2, pygame.Mask)

    dx = rect2.x - rect1.x
    dy = rect2.y - rect1.y
    offset = (dx, dy)

    return mask1.overlap(mask2, offset)

def getinstance(obj: object,
                kind: type) -> Optional[object]:
    """
    Looks for a type in an object's attributes. If the type is found, it returns the object.
    Otherwise, None is returned.

    Args:
        obj (object): The object to check.
        kind (type): The type of object to look for.

    Returns:
        Optional[object]: The first object of the given type in the attributes. If none is found, None is returned.

    Raises:
        TypeError: If the kind argument is not a type.
        warning: If the object has no attributes of the given type, or no attributes at all.

    Examples:
        >>> getinstance(pygame.sprite.Sprite(), pygame.Mask)
        pygame.Mask()
        >>> getinstance(pygame.Rect(), pygame.Mask)
        None
    """

    if not hasattr(obj, "__dict__"):
        logger.warning(f"Object {obj.__class__.__name__} has no attributes.")
        return None

    if isinstance(obj, kind):
        return obj
    for attr in obj.__dict__.values():
        if isinstance(attr, kind):
            return attr

    logger.warning(f"Object {obj.__class__.__name__} has no attribute with type {kind.__class__.__name__}")
    return None
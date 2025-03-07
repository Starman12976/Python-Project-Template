"""
states.py
---------
This file contains the logic and functions for each state of the program, including the menu and project
windows. The State objects control event handling, updating objects, and drawing to the screen.
"""

import logging
import pygame
from typing import List, Optional

logger = logging.getLogger(__name__)

class State:
    """
    Base class for all states.

    attributes:
        next_state (str): Used by the StateManager to transition between states.
    """
    def __init__(self) -> None:
        """
        Creates a State instance.
        """
        self.next_state: Optional[str] = None

        self.handlers = {
            pygame.QUIT: self.quit,
            pygame.KEYDOWN: self.handle_keydown,
            pygame.KEYUP: self.handle_keyup,
            pygame.MOUSEBUTTONDOWN: self.handle_mousebuttondown,
            pygame.MOUSEBUTTONUP: self.handle_mousebuttonup,
            pygame.MOUSEMOTION: self.handle_mousemotion,
            pygame.MOUSEWHEEL: self.handle_mousewheel
        }

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Base method for event handling.
        :param events: List of pygame events.
        :return: None.
        """
        for event in events:
            handler = self.handlers.get(event.type, lambda e: logger.debug(f"Event not handled: {e.type}"))
            handler(event)

    def update(self) -> None:
        """
        Base method for updating objects.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' updates nothing.")

    def draw(self, screen: pygame.Surface) -> None:
        """
        Base class for rendering.
        :param screen: PyGame display surface.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' draws nothing.")

    def handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Base method for keydown events.
        :param event: Keydown event.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' is not processing keydown events.")

    def handle_keyup(self, event: pygame.event.Event) -> None:
        """
        Base method for keyup events.
        :param event: Keyup event.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' is not processing keyup events.")

    def handle_mousebuttondown(self, event: pygame.event.Event) -> None:
        """
        Base method for mousebuttondown events.
        :param event: Mousebuttondown event.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' is not processing mousebuttondown events.")

    def handle_mousebuttonup(self, event: pygame.event.Event) -> None:
        """
        Base method for mousebuttonup events.
        :param event: Mousebuttonup event.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' is not processing mousebuttonup events.")

    def handle_mousemotion(self, event: pygame.event.Event) -> None:
        """
        Base method for mousemotion events.
        :param event: Mousemotion event.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' is not processing mousemotion events.")

    def handle_mousewheel(self, event: pygame.event.Event) -> None:
        """
        Base method for mousewheel events.
        :param event: Mousewheel event.
        :return: None.
        """
        logger.debug(f"'{self.__class__.__name__}' is not processing mousewheel events.")

    def quit(self, event: Optional[pygame.event.Event] = None) -> None:
        """
        Quits the program by setting next_state to 'quit'.
        :event: PyGame event.
        :return: None.
        """
        logger.debug("Quit event detected")
        self.next_state = 'quit'

class MenuState(State):
    """
    Handles controls and drawing of the menu. Inherits State class.
    """
    def __init__(self) -> None:
        """
        Creates a MenuState instance.
        """
        super().__init__()

        logger.info("Menu state created")

class StateManager:
    """
    StateManager holds and manages all states of the program and transitions between states.

    attributes:
        self.states (dict): A dictionary that matches state names with their classes.
    """

    def __init__(self) -> None:
        """
        Creates a StateManager instance.
        """
        self.states: dict[str, Optional[State]] = {
            'menu': MenuState(),
            'quit': None
        }
        self.current_state = self.states['menu']

        logger.debug(f"State list: {self.states}")
        logger.info("State manager created")

    def change_state(self) -> int:
        """
        Checks if the current state has a next state set and transitions to that state if applicable.

        Attributes:
            new_state_key: The next state, aligns with values in StateManager.states.

        :return: 1 if the next state is 'quit' or an error occurs, 0 otherwise.
        """
        if self.current_state.next_state:
            new_state_key = self.current_state.next_state

            logger.info(f"Changing to state '{new_state_key}'")

            if new_state_key not in self.states:
                logger.error(f"State key '{new_state_key}' is not a valid state")
                return 1

            if new_state_key == 'quit':
                return 1

            self.current_state = self.states[new_state_key]
            self.current_state.next_state = None

            logger.debug(f"State changed to class '{self.current_state.__class__.__name__}'")

        return 0
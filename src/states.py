"""
states.py
---------
This file contains the logic and functions for each state of the program, including the menu and project
windows. The State objects control event handling, updating objects, and drawing to the screen.
"""

# Import modules
from abc import ABC, abstractmethod
import logging
import pygame
from typing import Callable, Dict, List, Optional

# Initialize modules
logger: logging.Logger = logging.getLogger(__name__)

# Define State class
class State(ABC):
    """
    Base class for all states.

    Attr:
        next_state (str): Used by the StateManager to transition between states.
    """

    def __init__(self) -> None:
        """
        Creates a State instance.

        Returns:
            None
        """

        # State attributes
        self.next_state: Optional[str] = None

        # Event handlers
        self.handlers: Dict[int, Callable[[pygame.event.Event], None]] = {
            pygame.QUIT: self.quit,
            pygame.KEYDOWN: self.handle_keydown,
            pygame.KEYUP: self.handle_keyup,
            pygame.MOUSEBUTTONDOWN: self.handle_mousebuttondown,
            pygame.MOUSEBUTTONUP: self.handle_mousebuttonup,
            pygame.MOUSEMOTION: self.handle_mousemotion,
            pygame.MOUSEWHEEL: self.handle_mousewheel
        }

    @abstractmethod
    def cleanup(self) -> None:
        """
        Base method for cleaning up resources.

        Returns:
            None
        """
        pass

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Base method for event handling. It does not need to be updated unless special events require handling.

        Args:
            events (List[pygame.event.Event]): List of PyGame events.

        Returns:
            None.
        """
        for event in events:
            handler: Callable[[pygame.event.Event], None] = (
                self.handlers.get(
                    event.type,
                    self._unhandled_method
                )
            )

            handler(event)

    @abstractmethod
    def update(self) -> None:
        """
        Base method for updating objects.

        Returns:
            None.
        """
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Base class for rendering.

        Args:
            screen (pygame.Surface): PyGame display surface.

        Returns:
            None.
        """
        pass

    def handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Base method for keydown events.

        Args:
            event (pygame.event.Event): KeyDown event.

        Returns:
            None.
        """
        pass

    def handle_keyup(self, event: pygame.event.Event) -> None:
        """
        Base method for KeyUp events.

        Args:
            event (pygame.event.Event): KeyUp event.

        Returns:
            None.
        """
        pass

    def handle_mousebuttondown(self, event: pygame.event.Event) -> None:
        """
        Base method for MouseButtonDown events.

        Args:
            event (pygame.event.Event): MouseButtonDown event.

        Returns:
            None.
        """
        pass

    def handle_mousebuttonup(self, event: pygame.event.Event) -> None:
        """
        Base method for MouseButtonUp events.

        Args:
            event (pygame.event.Event): MouseButtonUp event.

        Returns:
            None.
        """
        pass

    def handle_mousemotion(self, event: pygame.event.Event) -> None:
        """
        Base method for MouseMotion events.

        Args:
            event (pygame.event.Event): MouseMotion event.

        Returns:
            None.
        """
        pass

    def handle_mousewheel(self, event: pygame.event.Event) -> None:
        """
        Base method for MouseWheel events.

        Args:
            event (pygame.event.Event): MouseWheel event.

        Returns:
            None.
        """
        pass

    def quit(self, event: Optional[pygame.event.Event] = None) -> None:
        """
        Quits the program by setting next_state to 'quit'.

        Args:
            event (Optional[pygame.event.Event]): The PyGame event. None by default.

        Returns:
            None.
        """
        logger.debug("Quit event detected")
        self.next_state = 'quit'

    def _unhandled_method(self, event: pygame.event.Event) -> None:
        """
        Base method for unhandled events.

        Args:
            event (pygame.event.Event): Unhandled event

        Returns:
            None
        """
        logger.debug(f"Unhandled event: {event.type}")

class MenuState(State):
    """
    Handles controls and drawing of the menu. Inherits State class.

    Attributes:
        next_state (str): Used by StateManager to handle state changes.
    """

    def __init__(self) -> None:
        """
        Creates a MenuState instance.

        Returns:
            None.
        """

        # Initialize State class
        super().__init__()

        # Finish initialization
        logger.info("Menu state created")

    def cleanup(self) -> None:
        """
        Cleans up resources for the menu state.

        Returns:
            None.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """
        Handles drawing for the menu state.

        Args:
            screen (pygame.Surface): PyGame display surface.

        Returns:
            None.

        """
        pass

    def update(self) -> None:
        """
        Updates objects for the menu state.

        Returns:
            None.
        """
        pass

class StateManager:
    """
    StateManager holds and manages all states of the program and transitions between states.

    Attr:
        self.states (Dict[str, Optional[State]]): A dictionary that matches state names with their classes.
        current_state (State): The current state object being utilized.
    """

    def __init__(self) -> None:
        """
        Creates a StateManager instance.

        Returns:
            None.
        """

        # State attributes
        self.MENU_KEY: str = 'menu'
        self.QUIT_KEY: str = 'quit'
        self.states: dict[str, Optional[State]] = {
            self.MENU_KEY: MenuState(),
            self.QUIT_KEY: None # Only used for exiting the game loop. Don't set another state to None.
        }
        self.current_state: State = self.states[self.MENU_KEY]

        # Finish initialization
        logger.debug(f"State list: {self.states}")
        logger.info("State manager created")

    def change_state(self) -> int:
        """
        Checks if the current state has a next state set and transitions to that state if applicable.

        Returns:
            int: 0 if the state has not changed or has been changed properly. 1 if the program is quitting or an error occurred.

        Raises:
            KeyError: If current_state.next_state is not one of the keys in StateManager.states.
        """

        # Determine if a state change is occurring
        if self.current_state.next_state is not None:
            # Get next state key. Must match key of StateManager.states
            new_state_key: str = self.current_state.next_state
            logger.info(f"Changing to state '{new_state_key}'")

            if new_state_key not in self.states:
                logger.error(f"State key '{new_state_key}' is not a valid state")
                return 1

            if new_state_key == self.QUIT_KEY:
                return 1

            self.current_state = self.states[new_state_key]
            self.current_state.next_state = None

            logger.debug(f"State changed to class '{self.current_state.__class__.__name__}'")

        return 0

    def cleanup(self) -> None:
        """
        Ensures all states have exited properly.
        """
        for state in self.states.values():
            if state is not None:
                try:
                    state.cleanup()
                except Exception as e:
                    logger.exception(f"An exception has occurred while cleaning up resources for "
                                     f"{state.__class__.__name__}. Exception: {e}")
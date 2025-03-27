"""
program.py
----------
This file holds the Program class that is used to handle all program behavior, including event handling,
updating objects, and drawing to the screen.
"""

# Import modules
from src.checks import is_boolean, is_integer, is_positive, is_sequence, is_valid_pygame_color
from src.functions import load_settings, get_display_size
import logging
import pygame
from states import StateManager
from types import TracebackType
from typing import Any, Dict, List, Optional, Type

# Initialize modules
logger: logging.Logger = logging.getLogger(__name__)
pygame.init()

# Define Program class
class Program:
    """
    Used to handle all program behavior, including event handling, updating objects, and drawing to the
    screen.

    Attr:
        screen (Surface) - Program window.
        dt (float) - Time (in seconds) since clock.tick() has been called.
        events (List[pygame.event.Event]) - List of events.
    """

    def __init__(self) -> None:
        """
        Creates a Program instance.

        Returns:
            None

        Raises:
            FileNotFoundError: If the program.json file is missing in src/Settings.
            JsonDecodeError: If the program.json file is not formatted properly.
            TypeError: See _validate_settings
            ValueError: See _validate_settings
        """

        # Get settings
        self.settings: Dict[str, Any] = load_settings('program')

        # Screen settings
        self.background_color: pygame.Color = self.settings['background_color']
        self.fullscreen: bool = self.settings['fullscreen']
        self.screen_size: tuple[int, int] = get_display_size() if self.fullscreen else self.settings['screen_size']

        # Clock settings
        self.fps: int = self.settings['fps']

        # Check for valid settings
        self._validate_settings()

        # Objects
        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_size); logger.info("Screen initialized")
        self.clock: pygame.time.Clock = pygame.time.Clock(); logger.info("Clock initialized")
        self.state_manager: StateManager = StateManager(); logger.info("State machine initialized")

        # Window attributes
        self.icon = pygame.image.load("src/Assets/Images/icon.png")
        self.title = self.settings['title']

        # Clock attributes
        self.dt: float = 0  # Measured in seconds; amount of time since last clock.tick() call.

        # Events
        self.events: List[pygame.event.Event] = []
        self.running: bool = False

        # Program attributes
        self.exit_code = 0

        # Finish initialization
        logger.info("Program instance created")

    def __enter__(self) -> "Program":
        """
        Handles context.

        Returns:
            Program: The Program instance.
        """

        # Enter Program context
        logger.debug("Entering Program context")

        # Return Program instance
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        """
        Cleans up resources when the program is done.

        Args:
            exc_type (Optional[Type(BaseException)]): The exception type.
            exc_value (Optional[BaseException]): The exception value.
            traceback (Optional[TracebackType]): The exception traceback.

        Returns:
            None
        """

        # Cleanup resources
        self.cleanup()

    def cleanup(self) -> None:
        """
        Cleans up any remaining resources.

        Returns:
            None
        """
        logger.info("Cleaning up resources...")

        # Cleanup resources
        try:
            self.state_manager.cleanup()
        except Exception as e:
            logger.error(f"Error while cleaning up resources for state manager: {e}")

        # Exit modules
        pygame.quit()
        logger.info(f"Modules exited successfully.")

    def run(self) -> int:
        """
        Starts the program loop.

        Returns:
            int: 0, if exited properly. 1, if an exception occurs.
        """

        # Start program loop
        logger.info("Program started!")

        # Set window attributes
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.title)

        self.running = True
        try:
            while self.running:
                # Get events
                self.events = pygame.event.get()

                # Determine if the program is exiting. Used in case the state event check fails.
                event_types: set[int] = {event.type for event in self.events}
                if pygame.QUIT in event_types:
                    self.running = False

                # Handle events
                self.state_manager.current_state.handle_events(self.events)

                # Update objects
                self.state_manager.current_state.update()

                # Draw frame
                self.screen.fill(self.background_color)
                self.state_manager.current_state.draw(self.screen)

                # Change states
                quit_occurred: int = self.state_manager.change_state()
                if quit_occurred:
                    self.running = False
                    break

                # Update display
                pygame.display.update()
                self.dt = self.clock.tick(self.fps) / 1000 # tick() returns milliseconds; convert to seconds
        except Exception:
            logger.exception("Fatal error in program loop. Exiting...")

            # Error exit code
            self.exit_code = 1
        finally:
            # Break the program loop
            logger.info("Breaking loop...")

            # Return exit code
            return self.exit_code

    def _validate_settings(self) -> None:
        """
        Ensures that the program settings are valid values.

        Returns:
            None.

        Raises:
            ValueError: See function.
            TypeError: See function.
        """

        # Check for valid settings
        if not is_valid_pygame_color(self.background_color):
            raise ValueError(f"Program background color setting is not a valid pygame color. "
                             f"Color given: {self.background_color}")
        if not is_boolean(self.fullscreen):
            raise TypeError(f"Program fullscreen setting is not a boolean. "
                            f"Value given: {self.fullscreen}")
        if not is_sequence(self.screen_size, 2):
            raise ValueError(f"Program screen size is not a sequence of two values. Given sequence: {self.screen_size}")
        for dimension in self.screen_size:
            if not is_integer(dimension):
                raise TypeError(f"Program screen size dimension is not an integer. "
                                f"Value given: {dimension}")
            if not is_positive(dimension):
                raise ValueError(f"Program screen size dimension is not positive. "
                                 f"Value given: {dimension}")
        if not is_integer(self.fps):
            raise TypeError(f"Program fps setting is not an integer. "
                             f"Value given: {self.fps}")
        if not is_positive(self.fps):
            raise ValueError(f"Program fps setting is not positive. "
                             f"Value given: {self.fps}")
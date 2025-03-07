"""
program.py
----------
This file holds the Program class that is used to handle all program behavior, including event handling,
updating objects, and drawing to the screen.
"""

from functions import load_settings, get_display_size
import logging
import pygame
from states import StateManager
from types import TracebackType
from typing import Optional, Type

logger = logging.getLogger(__name__)

class Program:
    """
    Used to handle all program behavior, including event handling, updating objects, and drawing to the
    screen.

    attributes:
        screen (Surface) - Program window
        running (bool) - Turns the program loop on/off.
    """

    def __init__(self) -> None:
        """
        Creates a Program instance.
        """
        self.settings = load_settings('program')
        self.state_manager = StateManager()

        self.fullscreen = self.settings['fullscreen']
        self.screen_size = get_display_size() if self.fullscreen else self.settings['screen_size']
        self.fps = self.settings['fps']

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        logger.info("Screen initialized")
        logger.debug(f"Screen size: {self.screen.get_size()}")
        logger.info("Clock initialized")
        logger.debug(f"fps: {self.fps}")

        self.events = []
        self.running = False

        logger.info("Program instance created")

    def __enter__(self) -> "Program":
        """
        Handles context.
        :return: Program instance
        """
        logger.debug("Entering Program context")
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        """
        Cleans up resources when the program is done.
        :param exc_type: Optional; the exception type.
        :param exc_value: Optional; the exception value.
        :param traceback: Optional; the exception traceback.
        """
        self.cleanup()

    def cleanup(self) -> None:
        logger.info("Cleaning up resources...")

        pygame.quit()

    def run(self) -> int:
        """
        Starts the program loop.
        :return: 0 if exited properly.
        """
        logger.info("Program started!")

        self.running = True
        while self.running:
            # Get events
            self.events = pygame.event.get()

            # Determine if the program is exiting
            if any(event.type == pygame.QUIT for event in self.events):
                self.running = False

            # Handle events
            self.state_manager.current_state.handle_events(self.events)

            # Update objects
            self.state_manager.current_state.update()

            # Draw frame
            self.state_manager.current_state.draw(self.screen)

            # Change states
            self.state_manager.change_state()

            # Update display
            pygame.display.update()
            self.clock.tick(self.fps)

        logger.info("Breaking loop...")

        return 0
"""
This is the entrance point for the program. If this file is executed directly, the main() function will execute.
"""

# Import modules
import logging
import os
from program import Program
import signal
import sys
from types import FrameType
from typing import Optional

# Initialize modules
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="program.log",
    filemode='w'
)
logger: logging.Logger = logging.getLogger(__name__)
logger.info("Imports finished")

def handle_sigterm(signum: int,
                   frame: Optional[FrameType]) -> None:
    """
    Handles a forced closing.

    Args:
        signum (int): Number of the sigterm.
        frame (Optional[FrameType]): Execution frame.

    Returns:
        None
    """

    # Get the program ID
    caller_pid: int = os.getpid()
    logger.warning(f"Received SIGTERM from process {caller_pid}, attempting shutdown...")

    # Exit modules
    logging.shutdown()

    # Exit program
    sys.exit(130)

# Ensure sigterm is handled
signal.signal(signal.SIGTERM, handle_sigterm)

# Main function of the program. Called automatically if this file is executed
def main() -> int:
    """
    The entry point for the program.

    Returns:
        int: The exit code of the program.
    """

    try:
        with Program() as program:
            # If exited properly, run() will return 0
            exit_code: int = program.run()
    except KeyboardInterrupt:
        logger.warning("Program interrupted")

        # Exit code 130 means there was a keyboard interrupt.
        exit_code = 130
    except Exception:
        logger.exception("An error occurred")

        # Exit code 1 means an error occurred
        exit_code = 1
    finally:
        logger.info("Shutting down...")

        # Exit modules
        logging.shutdown()

    # Return exit code
    return exit_code

# Ensure that the program is being executed directly
if __name__ == "__main__":
    # Start the program
    exit_code: int = main()

    # Exit the program
    logger.info(f"Exiting with code {exit_code}")
    sys.exit(exit_code)
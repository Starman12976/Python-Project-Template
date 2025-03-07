"""
This is the entrance point for the program.
"""

# Import modules
import logging
from program import Program
import signal
import sys
import types

# Initialize modules
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="program.log",
    filemode='w'
)
logger = logging.getLogger(__name__)
logger.info("Imports finished")

def handle_sigterm(signum: int,
                   frame: types.FrameType | None) -> None:
    logger.info("Received SIGTERM, shutting down...")
    # Ensure cleanup even if main() hasn't taken over
    logging.shutdown()
    sys.exit(130)

signal.signal(signal.SIGTERM, handle_sigterm)

def main():
    """
    The entry point for the program.
    """
    try:
        with Program() as program:
            # If exited properly, run() will return 0
            exit_code = program.run()
    except KeyboardInterrupt:
        logger.warning("Program interrupted as warning.")
        exit_code = 130
    except Exception:
        logger.exception("An error occurred")
        # Exit code 1 means an error occurred
        exit_code = 1
    finally:
        logger.info("Shutting down...")
        # Exit modules
        logging.shutdown()

    return exit_code

# Ensure that the program is being executed directly
if __name__ == "__main__":
    sys.exit(main())
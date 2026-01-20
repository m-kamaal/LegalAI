#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

def main():
    """
    Configures and demonstrates basic Python logging.
    """
    # 1. Configure the logging system
    # This sets up the default logger to write messages to the console (stderr).
    # The 'level=logging.INFO' ensures that only messages of INFO severity 
    # (and higher, like WARNING, ERROR, CRITICAL) are displayed.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 2. Log some messages
    logging.debug("This is a DEBUG message. It will NOT be shown by default.")
    logging.info("This is an INFO message. It provides general information.")
    logging.warning("This is a WARNING message. Something unexpected happened.")
    logging.error("This is an ERROR message. The program failed to do something.")
    logging.critical("This is a CRITICAL message. The program might stop now.")

if __name__ == "__main__":
    main()

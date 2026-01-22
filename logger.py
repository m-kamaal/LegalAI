import logging
from colorlog import ColoredFormatter
import sys

class ColorRuleFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()

        # Default color (neutral)
        record.log_color = "white"

        # --- semantic rules (order matters) ---

        if "Input state:" in msg:
            record.log_color = "green"

        elif "FINAL GRAPH STATE" in msg:
            record.log_color = "magenta"

        return True


def setup_logging(level=logging.DEBUG):
    handler = logging.StreamHandler(sys.stdout)

    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s%(reset)s"
    )

    handler.setFormatter(formatter)
    handler.addFilter(ColorRuleFilter())

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.handlers.clear()
    root.addHandler(handler)

    # Silence infra noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("posthog").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.WARNING)

import functools
from typing import Callable
import logging

def log_node(node_name: str):
    logger = logging.getLogger(f"langgraph.{node_name}")

    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(state: dict):
            logger.info("ENTER %s", node_name)
            logger.debug("Input state: %s", state)

            output = fn(state)

            logger.debug("Output: %s", output)
            logger.info("EXIT %s", node_name)
            return output
        return wrapper
    return decorator


"""Initializer for Flask Authentic Package

   Sets up Config and Logger for the rest of the codebase.
"""

import logging

from protean.conf import active_config

from . import config

__version__ = '0.0.11'

# Update the config here so that loading the repo will load the config
active_config.update_defaults(config)

# Set up the logger
logger = logging.getLogger('flask_authentic')

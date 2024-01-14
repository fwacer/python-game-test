"""
Author: Bryce Dombrowski
Contact: brycedombrowski.com/contact
Date: 2024-01-03
"""

import sys
import logging
import logging.handlers
import pygame

from data.main import main

def setup_root_logger():

    root_logger = logging.getLogger()
    log_level = logging.DEBUG
    root_logger.setLevel(log_level)
    
    format_str = '%(levelname)s:%(name)s: %(message)s (%(asctime)s; %(filename)s:%(lineno)d)'
    formatter = logging.Formatter(fmt=format_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.handlers.RotatingFileHandler('game.log', encoding='utf8', backupCount=1, maxBytes=100000)
    console_handler = logging.StreamHandler()

    for handler in [file_handler, console_handler]:
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    return root_logger

if __name__ == "__main__":
    root_logger = setup_root_logger()
    main()
    pygame.quit()
    sys.exit()
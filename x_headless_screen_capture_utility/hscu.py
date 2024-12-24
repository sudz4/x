import os
import time
import subprocess
from datetime import datetime
import pyfiglet

def create_screen_capture_directory():
    # Create a directory to store the screen captures
    directory = "/Users/sudz4/Desktop/X/x/x_headless_screen_capture_utility/hscu_output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
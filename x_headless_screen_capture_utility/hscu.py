import os
import time
import subprocess
from datetime import datetime
import pyfiglet

def create_screen_capture_dir(root_folder="/Users/sudz4/Desktop/X/x/x_headless_screen_capture_utility/hscu_outputs/"):
    # Create the root directory if it doesn't exist
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    
    # Create timestamp-based directory structure
    timestamp = datetime.now()
    date_folder = timestamp.strftime('%Y%m%d')  # Date folder (YYYYMMDD)
    
    # Create the date directory
    date_path = os.path.join(root_folder, date_folder)
    if not os.path.exists(date_path):
        os.makedirs(date_path)

    # Create the second op_level folder
    project_name = "myprojectname"
    project_path = os.path.join(date_path, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    return project_path

# Example usage
output_dir = create_screen_capture_dir()
print(f"Created directory: {output_dir}")
import os
import time

def wait_for_file(file_path, timeout=5):
    """Wait up to `timeout` seconds for the file to be fully written."""
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            return False  # File did not appear within timeout
        time.sleep(0.5)  # Check every 0.5 seconds
    return True
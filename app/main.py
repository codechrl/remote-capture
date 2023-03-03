import multiprocessing
import os
import time

import settings
from util import time_now

root_dir = settings.project_dir


def remote_capture():
    """remote capture"""
    os.system("python remote_capture.py")


def save_db_postgre():
    """save file"""
    os.system("python save_db_postgre.py")


# Create a list of functions
funcs = [remote_capture, save_db_postgre]

try:
    # Directory path
    dirs = ["/data", "/data/pcap"]

    # Create directory if it doesn't exist
    for dir in dirs:
        dir_path = root_dir + dir
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"{time_now()}  INFO\t: Directory '{dir}' created successfully")

    # Create a process for each function and start them
    processes = [multiprocessing.Process(target=func) for func in funcs]
    for process, func in zip(processes, funcs):
        process.start()
        print(f"{time_now()}  INFO\t: Sucessfully Started {func}")
        time.sleep(1)

except Exception as e:
    print(f"{time_now()}  ERROR\t: {str(e)}")

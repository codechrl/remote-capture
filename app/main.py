import multiprocessing
import os
import time

import settings
from util import time_now

root_dir = settings.project_dir


def remote_capture():
    """remote capture"""
    os.system("python remote_capture.py")


def extract():
    """extract"""
    os.system("python extract.py")


def save_file():
    """save file"""
    os.system("python save_file.py")


def save_http_file():
    """save http file"""
    os.system("python save-http-file.py")


def save_http_db():
    """save http db"""
    os.system("python save-http-db.py")


def cleaner():
    """cleaner"""
    os.system("python cleaner.py")


# Create a list of functions
funcs = [
    cleaner,
    remote_capture,
    extract,
    save_file,
    # save_http_file,
    # save_http_db,
]

try:
    # Directory path
    dirs = ["/data", "/data/pcap", "/data/json"]

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

    time.sleep(120)

    # Terminate all processes
    for process in processes:
        process.terminate()
        print(f"{time_now()}  INFO\t: Sucessfully Terminated {str(process)}")

except Exception as e:
    print(f"{time_now()}  ERROR\t: {str(e)}")

# finally:
#     # Terminate all processes
#     for process in processes:
#         process.terminate()
#     pass

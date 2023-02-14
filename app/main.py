import multiprocessing
import os
from datetime import datetime

# Function
def time_now(friendly = False):
    now = datetime.now()
    if friendly:
        dt_string = now.strftime("%Y-%m-%d_%H:%M:%S")
    else:
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    return str(dt_string)

# Define the process
def remote_capture():
    os.system( "python remote-capture.py" )
    pass

def extract():
    os.system( "python extract.py" )
    pass

def save_file():
    os.system( "python save-file.py" )
    pass

def save_db():
    os.system( "python save-db.py" )
    pass

def cleaner():
    os.system( "python cleaner.py" )
    pass

# Create a list of functions
funcs = [ cleaner, remote_capture, extract, save_file]

try:
    # Create a process for each function and start them
    processes = [multiprocessing.Process(target=func) for func in funcs]
    for process, func in zip(processes, funcs):
        process.start()
        print(f"{time_now()}  INFO\t: Sucessfully Started {func}")
    
    time.sleep(10)
    # Terminate all processes
    for process in processes:
        process.terminate()

except Exception as e:
    print(f"{time_now()}  ERROR\t: {str(e)}")

finally:
    # Terminate all processes
    for process in processes:
        process.terminate()
from dotenv import load_dotenv
import paramiko
import time
from datetime import datetime
import os
import settings

root_dir = settings.project_dir

# function
def time_now(friendly = False):
    now = datetime.now()
    if friendly:
        dt_string = now.strftime("%Y-%m-%d_%H:%M:%S")
    else:
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    return str(dt_string)

# SSH login credentials for the remote server
hostname = settings.HOSTNAME
username = settings.USERNAME
password = settings.PASSWORD
port = settings.PORT

# Initialize the activity counter
activity_count = 0

# The number of activities to capture in each PCAP file
activity_threshold = 50

# Create a new SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password)
print(f"{time_now()}  INFO\t: Connected to Remote Server {hostname}")
print(f"{time_now()}  INFO\t: Listening")

# Start the main loop
while True:

    # Create a new PCAP file based on the current time
    current_time = time.strftime("%Y-%m-%d_%H:%M:%S")
    pcap_filename = root_dir+"/data/pcap/capture_" + current_time + ".pcap_"
    local_file = open(pcap_filename, "wb")

    # Capture the PCAP file on the remote server
    cmd = 'tcpdump -s 0 -U -w - '
    filter = "not port 22"
    stdin, stdout, stderr = client.exec_command(cmd+filter)

    # Write to file
    while True:
        data = stdout.read(1024)
        if len(data) == 0: break
        local_file.write(data)
        activity_count += 1

        # Check the activity count
        if activity_count >= activity_threshold:

            # Reset the activity counter
            activity_count = 0

            # Close the local file
            local_file.close()
            os.system(f"mv {pcap_filename} {pcap_filename[:-1]}")
            print(f"{time_now()}  INFO\t: Saved to {pcap_filename[:-1]}")
            break

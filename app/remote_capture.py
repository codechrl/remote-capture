import os
import time

import paramiko

import settings
from util import time_now

# Store root directory
root_dir = settings.project_dir

# SSH login credentials for the remote server
HOSTNAME = str(settings.HOSTNAME)
USERNAME = str(settings.USERNAME)
PASSWORD = str(settings.PASSWORD)
PORT = str(settings.PORT)

# Print ceredentials
print(f"{time_now()}  INFO\t: HOSTNAME {HOSTNAME}")
print(f"{time_now()}  INFO\t: USERNAME {USERNAME}")
print(f"{time_now()}  INFO\t: PASSWORD {PASSWORD}")
print(f"{time_now()}  INFO\t: PORT {PORT}")

# Initialize the activity counter
ACTIVITY_COUNT = 0

# The number of activities to capture in each PCAP file
ACTIVITY_THRESHOLD = 50

# Create a new SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(HOSTNAME, PORT, USERNAME, PASSWORD)
except paramiko.SSHException as e:
    client.get_transport().auth_password(HOSTNAME, PASSWORD)


print(f"{time_now()}  INFO\t: Connected to Remote Server {HOSTNAME}")
print(f"{time_now()}  INFO\t: Listening")

# Start the main loop
while True:

    # Create a new PCAP file based on the current time
    current_time = time.strftime("%Y-%m-%d_%H:%M:%S")
    pcap_filename = root_dir + "/data/pcap/capture_" + current_time + ".pcap_"
    local_file = open(pcap_filename, "wb")

    # Capture the PCAP file on the remote server
    CMD = "tcpdump -s 0 -U -w - "
    FILTER = "not port 22"
    stdin, stdout, stderr = client.exec_command(CMD + FILTER)

    while True:
        # Write to file
        data = stdout.read(1024)
        if len(data) == 0:
            break
        local_file.write(data)
        ACTIVITY_COUNT += 1

        # Check the activity count
        if ACTIVITY_COUNT >= ACTIVITY_THRESHOLD:

            # Reset the activity counter
            ACTIVITY_COUNT = 0

            # Close the local file
            local_file.close()
            os.system(f"mv {pcap_filename} {pcap_filename[:-1]}")
            print(f"{time_now()}  INFO\t: Saved to {pcap_filename[:-1]}")
            break

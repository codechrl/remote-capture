import os
from datetime import datetime

import pandas as pd

import settings
from util import add_to_dataframe, list_pcap_files, time_now

root_dir = settings.project_dir

# Define the directory where the pcap files are stored
directory = root_dir + "/data/pcap/"

while True:
    try:
        # Get a list of all the pcap files in the directory
        pcap_files = list_pcap_files(directory)

        # Load the existing dataframe or create a new one if it doesn't exist
        try:
            df = pd.read_csv(root_dir + "/data/file_status.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["filename"])
            df["extracted"] = False
            df["saved"] = False
            df["cleaned"] = False

        # Add the pcap files to the dataframe if they are not already in the "filename" column
        df = add_to_dataframe(pcap_files, df)

        # Extract pcap
        for idx, row in df.iterrows():
            if row["extracted"] is False:
                file = row["filename"].split(".")[0]
                cmd = f"pcapkit-cli {root_dir}/data/pcap/{file}.pcap --output {root_dir}/data/json/{file}.json --verbose --format json"
                os.system(cmd)
                df.at[idx, "extracted"] = True
                os.system("clear")

                # Save the updated dataframe to disk
                df.to_csv(root_dir + "/data/file_status.csv", index=False)
                print(f"{time_now()}  INFO\t: CSV FIle Status Updated")

    except Exception as e:
        print(f"{time_now()}  ERROR\t: {str(e)}")

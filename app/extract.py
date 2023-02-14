import os
import pandas as pd
from datetime import datetime
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

def list_pcap_files(directory):
    pcap_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pcap"):
                pcap_files.append(os.path.join(file))
    return pcap_files

def add_to_dataframe(pcap_files, dataframe):
    for file in pcap_files:
        if file not in dataframe['filename'].tolist():
            new_row = pd.DataFrame({'filename': [file],
                                     'extracted': False,
                                     'saved': False,
                                     'cleaned': False,
                                     })
            dataframe = pd.concat([dataframe, new_row], ignore_index=True)
    return dataframe

# Define the directory where the pcap files are stored
directory = root_dir+'/data/pcap/'

while True:
    try:
        # Get a list of all the pcap files in the directory
        pcap_files = list_pcap_files(directory)

        # Load the existing dataframe or create a new one if it doesn't exist
        try:
            df = pd.read_csv(root_dir+'/data/file_status.csv')
        except FileNotFoundError:
            df = pd.DataFrame(columns=['filename'])
            df['extracted'] = False
            df['saved'] = False
            df['cleaned'] = False

        # Add the pcap files to the dataframe if they are not already in the "filename" column
        df = add_to_dataframe(pcap_files, df)

        # Extract pcap
        for idx, row in df.iterrows():
            if row['extracted'] == False:
                file = row['filename'].split(".")[0]
                cmd = f"pcapkit-cli {root_dir}/data/pcap/{file}.pcap --output {root_dir}/data/json/{file}.json --verbose --format json"
                os.system(cmd)
                df.at[idx, 'extracted'] = True
                os.system("clear")

                # Save the updated dataframe to disk
                df.to_csv(root_dir+'/data/file_status.csv', index=False)
                print(f"{time_now()}  INFO\t: CSV Saved")

    except Exception as e:
        print(f"{time_now()}  ERROR\t: {str(e)}")
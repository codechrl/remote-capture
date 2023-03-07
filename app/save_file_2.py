import time

import pandas as pd
import settings
from pcap_handler import pcapHandler
from util import add_to_dataframe, columns, list_pcap_files, time_now

root_dir = settings.project_dir
directory = root_dir + "/data/pcap/"

while True:
    try:
        try:
            df_status = pd.read_csv(root_dir + "/data/file_status.csv")
            print(f"{time_now()}  INFO\t: Read file status")

        except FileNotFoundError:
            # Get a list of all the pcap files in the directory
            pcap_files = list_pcap_files(directory)

            # Load the existing dataframe or create a new one if it doesn't exist
            df_status = pd.DataFrame(columns=["filename"])
            df_status["extracted"] = False
            df_status["saved"] = False
            df_status["cleaned"] = False

            # Add the pcap files to the dataframe if they are not already in the "filename" column
            df_status = add_to_dataframe(pcap_files, df_status)
            print(f"{time_now()}  INFO\t: Created file status")

        try:
            df = pd.read_csv(root_dir + "/data/file_record.csv")
            print(f"{time_now()}  INFO\t: Read file record")
        except FileNotFoundError:
            print(f"{time_now()}  INFO\t: Created file record")
            df = pd.DataFrame()

        # print(df_status)

        for idx, row in df_status.iterrows():
            if row["extracted"] is False and row["saved"] is False:
                file = root_dir + "/data/pcap/" + row["filename"]
                print(f"{time_now()}  INFO\t: Read {file}")

                df_new = pcapHandler(file=file)
                df_new = df_new.to_DF()
                df_new = df_new.set_axis(columns, axis=1)

                df_new = pd.concat([df, df_new], ignore_index=True)

                # Save update for file record
                df_new.to_csv(root_dir + "/data/file_record.csv", index=False)
                df_new.to_excel(root_dir + "/data/file_record.xlsx", index=False)

                # Save update for file status
                df_status.at[idx, "saved"] = True
                df_status.to_csv(root_dir + "/data/file_status.csv", index=False)

    except Exception as e:
        print(str(e))
        time.sleep(2)

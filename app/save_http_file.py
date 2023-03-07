import json

import pandas as pd
import settings
from tqdm import tqdm
from util import time_now

root_dir = settings.project_dir

while True:
    # Read csv file status
    try:
        df_status = pd.read_csv(root_dir + "/data/file_status.csv")

        # Load the existing dataframe or create a new one if it doesn't exist
        try:
            df_save = pd.read_csv(root_dir + "/data/file_record.csv")
        except FileNotFoundError:
            df_save = pd.DataFrame()

        for idx, row in df_status.iterrows():
            if row["extracted"] is True and row["saved"] is False:
                # Read JSON file
                file = row["filename"].split(".")[0]
                f = open(f"{root_dir}/data/json/{ file }.json")
                print(f"{time_now()}  INFO\t: Scanning {file}")

                # Returns JSON object as a dictionary
                data = json.load(f)

                # Returns dict to pandas dataframe
                for k, v in tqdm(data.items()):
                    # Scan for HTTP Payload on Frame
                    try:
                        receipt = v["ethernet"]["ipv4"]["tcp"]["http"]["receipt"]
                        header = v["ethernet"]["ipv4"]["tcp"]["http"]["header"]
                        body = v["ethernet"]["ipv4"]["tcp"]["http"]["body"]

                        record = receipt | header | {"body": body}

                    except Exception:
                        pass

                    try:
                        df_temp = pd.DataFrame(record)
                        df_save = pd.concat([df_save, df_temp], ignore_index=True)
                        df_save.to_csv(root_dir + "/data/file_record.csv", index=False)
                        # df_save.to_excel(root_dir+'/data/file_record.xlsx', index=False)
                        # print(f"{time_now()}  INFO\t: Found HTTP Payload")

                    except Exception:
                        # print(str(e))
                        pass

                # Save update for file status
                df_status.at[idx, "saved"] = True
                df_status.to_csv(root_dir + "/data/file_status.csv", index=False)

    except:
        pass

import json
import time

import pandas as pd

import settings
from util import time_now

root_dir = settings.project_dir

while True:

    try:
        # Read csv file status
        df_status = pd.read_csv(root_dir + "/data/file_status.csv")

        # Load the existing dataframe or create a new one if it doesn't exist
        try:
            df_save = pd.read_csv(root_dir + "/data/file_record.csv")
            df_save_excel = pd.read_excel(root_dir + "/data/file_record.xlsx")
        except FileNotFoundError:
            df_save = pd.DataFrame()
            df_save_excel = pd.DataFrame()

        for idx, row in df_status.iterrows():
            if row["extracted"] and row["saved"] is False:

                # Read JSON file
                file = row["filename"].split(".")[0]
                f = open(f"{root_dir}/data/json/{ file }.json")
                print(f"{time_now()}  INFO\t: Scanning {file}")

                # Returns JSON object as a dictionary
                data = json.load(f)
                data = dict(data)

                try:
                    # Append new data to existing dataframe
                    df_new = pd.DataFrame(data).T
                    df_save = pd.concat([df_save, df_new], axis=1)
                    df_save = df_save.reset_index(drop=True)
                    df_save_excel = pd.concat([df_save_excel, df_new], axis=1)
                    df_save_excel = df_save_excel.reset_index(drop=True)

                    # Save update for file record
                    df_save.to_csv(root_dir + "/data/file_record.csv", index=False)
                    df_save_excel.to_excel(
                        root_dir + "/data/file_record.xlsx", index=False
                    )

                    # Save update for file status
                    df_status.at[idx, "saved"] = True
                    df_status.to_csv(root_dir + "/data/file_status.csv", index=False)

                except Exception as e:
                    print(str(e))
                    # pass

    except Exception as e:
        print(str(e))
        time.sleep(10)
        # pass

import os
import time

import pandas as pd

import settings
from util import time_now

time.sleep(10)

root_dir = settings.project_dir

while True:
    try:
        df = pd.read_csv(root_dir + "/data/file_status.csv")
        for idx, row in df.iterrows():
            try:
                if row["extracted"] and row["saved"]:
                    file = row["filename"].split(".")[0]
                    os.remove(f"{root_dir}/data/pcap/{ file }.pcap")
                    os.remove(f"{root_dir}/data/json/{ file }.json")
                    print(f"{time_now()}  INFO\t: Deleted {file}")

                    df.at[idx, "cleaned"] = True
                    df.to_csv(root_dir + "/data/file_status.csv", index=False)
                    print(f"{time_now()}  INFO\t: CSV Updated")

            except Exception as e:
                # print(f"{time_now()}  ERROR\t: {str(e)}")
                pass

    except Exception as e:
        # print(f"{time_now()}  ERROR\t: {str(e)}")
        pass

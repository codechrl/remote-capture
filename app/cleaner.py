import os
import pandas as pd
from datetime import datetime
import settings
import time

root_dir = settings.project_dir

# function
def time_now(friendly = False):
    now = datetime.now()
    if friendly:
        dt_string = now.strftime("%Y-%m-%d_%H:%M:%S")
    else:
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    return str(dt_string)

while True:
    try:
        df = pd.read_csv(root_dir+'/data/file_status.csv')
        for idx, row in (df.iterrows()):
            try:
                if row["extracted"] == True and row["saved"] == True:
                    file = row['filename'].split(".")[0]
                    os.remove(f"{root_dir}/data/pcap/{ file }.pcap")
                    os.remove(f"{root_dir}/data/json/{ file }.json")
                    print(f"{time_now()}  INFO\t: Deleted {file}")

                    df.at[idx, 'cleaned'] = True
                    df.to_csv(root_dir+'/data/file_status.csv', index=False)
                    print(f"{time_now()}  INFO\t: CSV Updated")
            
            except Exception as e:
                #print(f"{time_now()}  ERROR\t: {str(e)}")
                pass

    except Exception as e:
        #print(f"{time_now()}  ERROR\t: {str(e)}")
        pass

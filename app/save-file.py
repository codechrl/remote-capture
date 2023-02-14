import pandas as pd
import json
import time
import os
from tqdm import tqdm
from datetime import datetime

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

    # Read csv file status
    try:
        df_status = pd.read_csv(root_dir+"/data/file_status.csv")

        # Load the existing dataframe or create a new one if it doesn't exist
        try:
            df_save = pd.read_csv(root_dir+'/data/file_record.csv')
        except FileNotFoundError:
            df_save = pd.DataFrame()

        for idx, row in (df_status.iterrows()):
            if row["extracted"] == True and row["saved"] == False:

                # Read JSON file
                file = row['filename'].split(".")[0]
                f = open(f"{root_dir}/data/json/{ file }.json")
                print(f"{time_now()}  INFO\t: Scanning {file}")
                
                # Returns JSON object as a dictionary
                data = json.load(f)

                # Returns dict to pandas dataframe
                for k, v in tqdm(data.items()):

                    # Scan for HTTP Payload on Frame
                    try:
                        receipt = v['ethernet']['ipv4']['tcp']['http']['receipt']
                        header  = v['ethernet']['ipv4']['tcp']['http']['header']
                        body    = v['ethernet']['ipv4']['tcp']['http']['body']

                        record = (  receipt  |     \
                                    header   |     \
                                    {"body": body}
                                )
                                    
                    except Exception as e:
                        pass

                    try:
                        df_temp = pd.DataFrame(record)
                        df_save = pd.concat([df_save, df_temp], ignore_index=True)
                        df_save.to_csv(root_dir+'/data/file_record.csv', index=False)
                        df_save.to_excel(root_dir+'/data/file_record.xlsx', index=False)
                        #print(f"{time_now()}  INFO\t: Found HTTP Payload")

                    except Exception as e:
                        #print(str(e))
                        pass

                # Save update for file status
                df_status.at[idx, 'saved'] = True
                df_status.to_csv(root_dir+'/data/file_status.csv', index=False)
    
    except:
        pass
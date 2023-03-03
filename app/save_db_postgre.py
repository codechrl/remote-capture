import datetime
import json
import os
import time
import warnings

import pandas as pd
import settings
from pcap_handler import dfHandler, pcapHandler
from sqlalchemy import create_engine
from util import add_to_dataframe, columns, list_pcap_files, time_now

warnings.filterwarnings("ignore")

root_dir = settings.project_dir
directory = root_dir + "/data/pcap/"

engine = create_engine(settings.PGSTRING, echo=False)

while True:
    try:
        # Get a list of all the pcap files in the directory
        pcap_files = list_pcap_files(directory)

        for idx, row in enumerate(pcap_files):
            try:
                # read pcap file
                file = root_dir + "/data/pcap/" + row
                print(f"{time_now()}  INFO\t: Read {file}")

                # load to df
                df_new = pcapHandler(file=file)
                df_new = df_new.to_DF()
                df_new = df_new.set_axis(columns, axis=1)

                df = pd.DataFrame()
                df = pd.concat([df, df_new], ignore_index=True)

                # convert to conrresponding dtype
                df = df.convert_dtypes()
                df = df.astype(
                    {
                        "flags_fragment": str,
                        "timestamp": float,
                        "flags": str,
                        "payload_raw": str,
                        "payload_hex": str,
                    }
                )
                df["datetime"] = df["timestamp"].apply(
                    lambda d: datetime.date.fromtimestamp(d)
                )

                # save record to db
                df.to_sql(
                    "traffic",
                    con=engine,
                    method="multi",
                    if_exists="append",
                )
                print(f"{time_now()}  INFO\t: Saved to db {file}")

                # remove pcap file
                os.remove(file)
                print(f"{time_now()}  INFO\t: Deleted {file}")

            except Exception as e:
                print(f"{time_now()}  ERROR\t: Failed save to db {file} {str(e)}")

    except Exception as e:
        print(f"{time_now()}  ERROR\t: {str(e)}")
        time.sleep(5)

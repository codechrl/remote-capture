import json
import os
import time
from datetime import datetime

import influxdb_client
import pandas as pd
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from tqdm import tqdm

import settings
from util import time_now

root_dir = settings.project_dir

# Load environment variables from .env file
load_dotenv()
token = os.getenv("INFLUXDB_TOKEN")

# Connect to database
org = "remote_capture"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
print(f"{time_now()}  INFO\t: Connected to Database")

# Define the write api
bucket = "host-test"
write_api = write_client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        # Read csv file status
        df_status = pd.read_csv(root_dir + "/data/file_status.csv")

        for idx, row in df_status.iterrows():
            if row["extracted"] == True and row["saved"] == False:
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

                        http_payload = receipt | header | {"body": body}
                        # print(f"{time_now()}  INFO\t: Found HTTP Payload")

                    except Exception as e:
                        pass

                    try:
                        # Create point for influxdb
                        point = (
                            Point("activity")
                            .tag("host", "172.104.184.124")
                            .field("type", http_payload["type"])
                            .field("version", http_payload["version"])
                            .field("status", http_payload["status"])
                            .field("message", http_payload["message"])
                            .field("Date", http_payload["Date"])
                            .field("Server", http_payload["Server"])
                            .field("Location", http_payload["Location"])
                            .field("Content-Length", http_payload["Content-Length"])
                            .field("Keep-Alive", http_payload["Keep-Alive"])
                            .field("Connection", http_payload["Connection"])
                            .field("Content-Type", http_payload["Content-Type"])
                            # .field( "body", record["body"] )
                        )

                        # Write to influx db
                        write_api.write(bucket=bucket, org=org, record=point)

                    except Exception as e:
                        # print(str(e))
                        pass

                # Save update for file status
                df_status.at[idx, "saved"] = True
                df_status.to_csv(root_dir + "/data/file_status.csv", index=False)

    except:
        pass

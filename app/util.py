# Utility

import os
from datetime import datetime

import pandas as pd

columns = [
    "version",
    "ihl",
    "tos",
    "len",
    "id",
    "flags_fragment",
    "frag",
    "ttl",
    "proto",
    "chksum",
    "src",
    "dst",
    "options",
    "time",
    "sport",
    "dport",
    "seq",
    "ack",
    "dataofs",
    "reserved",
    "flags",
    "window",
    "chksum_payload",
    "urgptr",
    "options_payload",
    "payload",
    "payload_raw",
    "payload_hex",
]


def time_now(friendly=False):
    """get time now"""
    now = datetime.now()
    if friendly:
        dt_string = now.strftime("%Y-%m-%d_%H:%M:%S")
    else:
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

    return str(dt_string)


def list_pcap_files(directory):
    """get list of pcap file in a directory"""
    pcap_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pcap"):
                pcap_files.append(os.path.join(file))
    return pcap_files


def add_to_dataframe(pcap_files, dataframe):
    """pcap file to dataframe"""
    for file in pcap_files:
        if file not in dataframe["filename"].tolist():
            new_row = pd.DataFrame(
                {
                    "filename": [file],
                    "extracted": False,
                    "saved": False,
                    "cleaned": False,
                }
            )
            dataframe = pd.concat([dataframe, new_row], ignore_index=True)
    return dataframe

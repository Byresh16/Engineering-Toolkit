from datetime import datetime
import os
import sys
import configparser

class TimeStamp(object):
    def __init__(self, path):
        self.txt = path
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.ini')
        self.formats = None

    def load_timestamp_formats(self):
        cp = configparser.ConfigParser(interpolation=None)
        cp.read(self.config_path)

        if cp.has_section('timestamp') and cp.has_option('timestamp', 'formats'):
            raw = cp.get('timestamp', 'formats')
            formats = [f.strip() for f in raw.splitlines() if f.strip()]
            if formats:
                return formats
        return [
            "%d-%m-%Y_ %H_%M_%S",
            "%d-%m-%Y_%H_%M_%S",
            "%Y-%m-%d-%H-%M-%S",
            "%d-%m-%Y-%H-%M-%S",
            "%y%m%d%H%M%S",
            "%Y%m%d-%H%M%S",
            "%Y%m%d %H%M%S",
        ]

    def exttimestamp(self):
        self.formats = self.load_timestamp_formats()
        # formats = [
        #     "%d-%m-%Y_ %H_%M_%S",
        #     "%d-%m-%Y_%H_%M_%S",
        #     "%Y-%m-%d-%H-%M-%S",
        #     "%d-%m-%Y-%H-%M-%S",
        #     "%y%m%d%H%M%S",
        #     "%Y%m%d-%H%M%S"
        # ]
        # --- Extract timestamp and type ---
        if "bugreport" in self.txt:
            timestamp = self.txt[-19:]
            tag = "bugreport"
        elif "Android" in self.txt:
            timestamp = self.txt.split(".")[0].lstrip("[")
            tag = "Android"
        elif "ecs" in self.txt:
            timestamp = self.txt.split("_ecs")[0]
            tag = "ecs"
        elif "meminfo" in self.txt:
            timestamp = self.txt.split("_meminfo")[0]
            tag = "meminfo"
        elif "Dropbox" in self.txt:
            timestamp = self.txt.split(".")[0].lstrip("[")
            tag = "Dropbox"
        elif "teraterm" in self.txt:
            timestamp = self.txt.split("_")[1].split(".")[0]
            tag = "teraterm"
        elif "CAN" in self.txt:
            timestamp = self.txt.split("_")[1]
            tag = "can"
        else:
            raise ValueError("Unknown log type")
        # --- Convert to datetime ---
        for fmt in self.formats:
            try:
                dt = datetime.strptime(timestamp, fmt)
                final_time = dt.strftime("%Y%m%d %H%M%S")
                # print(final_time)
                # print(tag)
                return final_time, tag, self.txt
            except ValueError:
                continue
        raise ValueError("Unsupported date format: {}".format(timestamp))
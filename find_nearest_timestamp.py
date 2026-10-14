# -*- coding: utf-8 -*-

import os
from datetime import datetime
from extract_date_time import TimeStamp
class Find_folder():
   def __init__(self, subfolderpath, timestamp):
       self.root_path = subfolderpath
       self.target_timestamp = timestamp
   def dateextract(self, fname):
        clean_name = fname
        if ("bugreport" in fname) and fname.lower().endswith(".zip"):
            clean_name = fname[:-4]
        r = TimeStamp(clean_name).exttimestamp()
        if not r:
            return datetime.min
        ts_str = r[0].split(".")[0]  
        return datetime.strptime(ts_str, "%Y%m%d %H%M%S")

   def time_stamp_list(self):
       names = os.listdir(self.root_path)
       names.sort(key=self.dateextract)
       updatedtimestamps = []
       for name in names:
           clean_name = name
           if "bugreport" in name:
               clean_name = name[:-4]  # remove .zip if bugreport
           t = TimeStamp(clean_name)
           timestampwithtag = t.exttimestamp()
           # store tuple: (timestamp_str, tag, filename)
           updatedtimestamps.append((timestampwithtag[0], timestampwithtag[1], name))
       return updatedtimestamps
   def find_file(self):
       dt_target = datetime.strptime(self.target_timestamp, "%Y-%m-%d %H-%M-%S")
       updatedtimestamps = self.time_stamp_list()
       if "ecs" in self.root_path.lower():
           nearest_lower_ecs = []
           nearest_lower_meminfo = []
           nearest_bugreport = []
           for ts, tag, fname in updatedtimestamps:
               ts_clean = ts.split(".")[0]  # remove milliseconds if any
               dt = datetime.strptime(ts_clean, "%Y%m%d %H%M%S")
               if tag == "ecs":
                   if dt < dt_target:
                       nearest_lower_ecs.append(fname)                       
               elif tag == "meminfo":
                   if dt < dt_target:
                       nearest_lower_meminfo.append(fname)
               elif tag == "bugreport":
                   if dt > dt_target:
                       nearest_bugreport.append(fname)
           return nearest_lower_ecs[len(nearest_lower_ecs)-1] if nearest_lower_ecs else None, \
                  nearest_lower_meminfo[len(nearest_lower_meminfo)-1] if nearest_lower_meminfo else None, \
                  nearest_bugreport[0] if nearest_bugreport else None
       # For other folders → only one file
       else:
           lower = []
           higher = []
           for ts, tag, fname in updatedtimestamps:
               ts_clean = ts.split(".")[0]
               dt = datetime.strptime(ts_clean, "%Y%m%d %H%M%S")
               if tag in ("Android"):
                   if dt < dt_target:
                    #    print(dt)
                       lower.append(fname)
               elif tag  in ("teraterm"):
                   if dt < dt_target:
                    #    print(dt)
                       lower.append(fname)                
               elif tag in ("Dropbox"):
                   if dt > dt_target:
                       higher.append(fname)
               elif tag in ("can"):
                   if dt < dt_target:
                    #    print(dt)
                       lower.append(fname)
           if lower:
            #    print(lower)
               if tag in ("teraterm"):
                   return lower[len(lower)-1]
               elif tag in ("Android"):
                    return lower[len(lower)-1]
               elif tag in ("can"):
                    return lower[len(lower)-1]
           elif higher:
            #    print(higher)
               return higher[0]
           else:
               return None
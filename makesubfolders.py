import os
import shutil
LOG_FOLDERS = {
   "android": "Android_Logs_",
   "dropbox": "Dropbox_Logs_",
   "bugreport": "Bugreport_Logs_",
   "ecs": "Meminfo_ECS_Logs_",
   "teraterm" : "Teraterm_Logs_",
   "can" : "CAN_Logs_"
}
# SOURCE_ROOTS = {

#     "android": r"D:\99.Log\1.Renault_AndroidLog",
#     "dropbox": r"D:\99.Log\2.Renault_Dropbox_Log",
#     "ecs": r"D:\99.Log\4.ecs",
#     "teraterm" : r"D:\99.Log\5.Teraterm",
#     "can": 
# }
def subfolders(entry_folder, entry_sw,logger=None):
   for folder in LOG_FOLDERS.values():
       path = os.path.join(entry_folder, folder+entry_sw)
       os.makedirs(path, exist_ok=True)
       if logger:
           logger("Created {}".format(path))
def addlogs(logs_dict, entry_folder, entry_sw, entry_can, logger=None, source_roots=None):
   source_roots = source_roots or {
       "android": r"D:\99.Log\1.Renault_AndroidLog",
       "dropbox": r"D:\99.Log\2.Renault_Dropbox_Log",
       "ecs": r"D:\99.Log\4.ecs",
       "teraterm": r"D:\99.Log\5.Teraterm",
       "can": entry_can,
   }
   for source, logs in logs_dict.items():
       for log in logs or []:
           if not log:
               continue
           src_root = source_roots.get(source, entry_can if source == "can" else "")
           if source == "android":
               dst_root = "Android_Logs_" + entry_sw
           elif source == "dropbox":
               dst_root = "Dropbox_Logs_" + entry_sw
           elif source == "teraterm":
               dst_root = "Teraterm_Logs_" + entry_sw
           elif source == "can":
               dst_root = "CAN_Logs_" + entry_sw
           elif "bugreport" in log.lower():
               dst_root = "Bugreport_Logs_" + entry_sw
           else:
               dst_root = "Meminfo_ECS_Logs_" + entry_sw

           src_path = os.path.join(src_root, log)
           dst_path = os.path.join(entry_folder, dst_root, log)
           try:
               if os.path.isfile(src_path):
                   shutil.copy2(src_path, dst_path)
               elif os.path.isdir(src_path):
                   shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
               else:
                   if logger:
                       logger("Skipped missing source: {}".format(src_path))
                   continue
               if logger:
                   logger("Copied [{}]: {}".format(source, log))
           except Exception as exc:
               if logger:
                   logger("Copy failed [{}] {}: {}".format(source, log, exc))

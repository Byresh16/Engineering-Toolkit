from find_nearest_timestamp import Find_folder
from canlog import extractcanlogs
import os
from extract_date_time import TimeStamp
from datetime import datetime


class All_Logs():
   def __init__(self,logfolder,targettimestamp):
       self.root_folder=logfolder
       self.targettimestamp=targettimestamp
       self.names = os.listdir(self.root_folder)
       self.names.sort()



   def threelogs(self,logger=None):
       result=[]
       f=Find_folder(self.root_folder, self.targettimestamp)

       if ("ecs") in self.root_folder:
           res=[]
           issueecs, issuememinfo, issuebugreport=f.find_file()
           res.append(self.names[self.names.index(issueecs)-3:self.names.index(issueecs)+4])
           res.append(self.names[self.names.index(issuebugreport)-1:self.names.index(issuebugreport)+2])
           for sublist in res:
               result.extend(sublist)
       if ("Android") in self.root_folder:
           res=[]
           res.append(self.names[self.names.index(f.find_file())-1:self.names.index(f.find_file())+2])
           for sublist in res:
               result.extend(sublist)
       if ("Dropbox") in self.root_folder:
           res=[]
           res.append(self.names[self.names.index(f.find_file())-1:self.names.index(f.find_file())+2])
           for sublist in res:
               result.extend(sublist)
       if("Teraterm") in self.root_folder:
           res=[]
           res.append(self.names[self.names.index(f.find_file())-1:self.names.index(f.find_file())+1])
           for sublist in res:
               result.extend(sublist)
       if("LOG_CAN") in self.root_folder:
           return extractcanlogs(self.root_folder,self.targettimestamp)
           
    #    logger(str(result))
        
       return result
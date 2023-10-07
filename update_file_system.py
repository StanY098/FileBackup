import os
import os.path as path
import subprocess
import platform
from datetime import datetime as dt
from win11toast import toast
import configparser

#write a function Toast to show notification
def Toast(message):
    toast('Update File Notification', message)

#write a function to write logs
def WriteLog(message):
    try:
        filename = "update_file_log.log"
        datetime_str = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(filename, "a")
        f.write("[" + datetime_str + "] " + message + "\n")
        f.close()
    except:
        Notification("An exception occurred on writing logs.")

#writw a function names Notification to print, Toast and WriteLog if each function flag is True
def Notification(message, isPrint=True, isToast=True, isWriteLog=True):
    if isPrint:
        print(message)
    if isToast:
        Toast(message)
    if isWriteLog:
        WriteLog(message)

#write a function to copy a file (not a directory and not include subdirectories) from source to destination based on different OS system, including Windows, Linux and Mac; if Windows and prompted, always 'F' for answer for xcopy
def Copy(src, dest):
    result = 0
    try:
        if platform.system() == "Windows":
            subprocess.run(["xcopy", src, dest + "*", "/Y"])
        elif platform.system() == "Linux":
            subprocess.run(["cp", src, dest])
        elif platform.system() == "Darwin":
            subprocess.run(["cp", src, dest])
        else:
            Notification("Unknown OS system.")
            result = 1
    except Exception as e:
        Notification("[Copy] occurred an error: " + str(e))
        result = 1
    return result

#write a function to update file
def UpdateFile(src, dest_path, last_update_date):
    result = 0
    try:
        if path.exists(src) and path.exists(dest_path):
            if path.isdir(src) and path.isdir(dest_path):
                for root, dirs, files in os.walk(src):
                    for file in files:
                        src_file = path.join(root, file)
                        if dt.fromtimestamp(path.getmtime(src_file)) > dt.strptime(last_update_date, "%d/%m/%Y"):
                            dest_file = path.join(dest_path, path.relpath(src_file, src))
                            if Copy(src_file, dest_file) == 0:
                                Notification("Copy " + src_file + " to " + dest_file + " successfully.")
                            else:
                                Notification("Copy " + src_file + " to " + dest_file + " failed.")
                                result = 1
            else:
                Notification(src + " or " + dest_path + " is not a directory.")
        else:
            Notification(src + " or " + dest_path + " is not found.")
    except Exception as e:
        Notification("[UpdateFile] occurred an error: " + str(e))
    return result

#write a function to get last update date from destination and if not found, create a new one
def GetLastUpdateDate(dest):
    date_filename = "lastUpdateDate.txt"
    last_update_date = dt.now().strftime("%d/%m/%Y")
    
    try:
        if path.exists(dest):
            if path.isdir(dest):
                filename = path.join(dest, date_filename)
                if path.exists(filename):
                    f = open(filename, "r")
                    last_update_date = f.read()
                    f.close()
                else:
                    f = open(filename, "w")
                    f.write(last_update_date)
                    f.close()
            else:
                Notification(dest + " is not a directory.")
        else:
            Notification(dest + " is not found.")
    except Exception as e:
        Notification("[GetLastUpdateDate] occurred an error: " + str(e))
    return last_update_date

#write a function to get last update date from destination
def UpdateLastUpdateDate(dest_path):
    date_filename = "lastUpdateDate.txt"
    
    try:
        if dest_path == "c:\\Users\stanl.STANLEY\OneDrive":
            dest_path = dest_path + "\Documents"
        filename = path.join(dest_path, date_filename)
        f = open(filename, "w")
        update_date = dt.now().strftime("%d/%m/%Y")
        f.write(update_date)
        f.close()
    except Exception as e:
        Notification("[UpdateLastUpdateDate] occurred an error: " + str(e))

#===============================================================================================================

Toast("Updating...")

#write a function to get all config in FileBackup.ini by configparser
config = configparser.ConfigParser()
config.read('FileBackup.ini')

#get path value from SRCPATH from config, and convert to string
src = str(config['SRCPATH']['path'])

#loop through config['TGTPATH'] to get all keys and values and put them into a dictionary named "tgts"
tgts = {}
for key in config['TGTPATH']:
    tgts[key] = config['TGTPATH'][key]

#loop through tgts to get value, then convert to string and then store all value into an array named "dests"
dests = []
for tgt in tgts.values():
    dests.append(str(tgt))

#loop through dests to update files
for dest in dests:
    if path.exists(src) and path.exists(dest):
        lastUpdateDate = GetLastUpdateDate(dest)
        result = UpdateFile(src, dest, lastUpdateDate)
        if result == 0:
            UpdateLastUpdateDate(dest)
    else:
        if not path.exists(src):
            Notification(src + " is not found.")
        if not path.exists(dest):
            Notification(dest + " is not found.")

Toast("Update Complete. Please see log for more details.")
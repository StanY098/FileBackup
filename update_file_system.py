import os
import os.path as path
import subprocess
import platform
from datetime import datetime as dt
from win11toast import toast

def Toast(message):
    toast('Update File Notification', message)

def WriteLog(message):
    try:
        filename = "update_file_log.log"
        datetime_str = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(filename, "a")
        f.write("[" + datetime_str + "] " + message + "\n")
        f.close()
    except:
        #print("An exception occurred on writing logs.")
        Toast("An exception occurred on writing logs.")

def Copy(src, dest):
    value = 0
    try:
        s = platform.system()
        if s == "Linux" or s == "Darwin":
            cmd = "copy \"" + src + "\" \"" + dest + "\""
            value = subprocess.call(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
            if value != 0:
                message = "[Copy] " + cmd + " : has error."
                #print(message)
                WriteLog(message)
                #Toast(message)
        elif s == "Windows":
            cmd = "copy \"" + src + "\" \"" + dest + "\""
            value = subprocess.call(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
            if value != 0:
                message = "[Copy] " + cmd + " : has error."
                #print(message)
                WriteLog(message)
                #Toast(message)
    except Exception as e:
        print(str(e) + ": " + cmd)
        WriteLog(str(e) + ": " + cmd)
        #Toast(str(e) + ": " + cmd)
        value = 1
    
    return value

def UpdateFile(source_path, dest_path, last_update_date):
    try:
        for name in os.listdir(source_path):
            try:
                f = path.join(source_path, name)
                
                #checking if it is a directory
                if path.isdir(f):
                    if path.exists(f):
                        dest_path_f = path.join(dest_path, name)
                        UpdateFile(f, dest_path_f, last_update_date)
                    else:
                        dest_f = path.join(dest_path, name)
                        value = Copy(f, dest_f)
                        if value == 0:
                            message = "[Copy] Success: " + f + " to " + dest_f
                            #print(message)
                            WriteLog(message)
                            Toast(message)
                
                #checking if it is a file
                elif path.isfile(f):
                    dest_f = path.join(dest_path, name)
                    if path.exists(dest_f):
                        m_date = dt.fromtimestamp(path.getmtime(f)).strftime("%Y/%m/%d")
                        if m_date != None and m_date > last_update_date:
                            value = Copy(f, dest_f)
                            if value == 0:
                                message = "[Copy] Success: " + f + " to " + dest_f
                                #print(message)
                                WriteLog(message)
                                Toast(message)
                    else:
                        value = Copy(f, dest_f)
                        if value == 0:
                            message = "[Copy] Success: " + f + " to " + dest_f
                            #print(message)
                            WriteLog(message)
                            Toast(message)
            except Exception as e:
                #print("[UpdateFile] " + name + " occurred an error. ", e)
                WriteLog("[UpdateFile] " + name + " occurred an error:" + str(e))
                Toast("[UpdateFile] " + name + " occurred an error:" + str(e))
    except Exception as e:
        #print("[UpdateFile] " + source_path + " occurred an error. ", e)
        WriteLog("[UpdateFile] " + source_path + " occurred an error:" + str(e))
        Toast("[UpdateFile] " + source_path + " occurred an error:" + str(e))

def GetLastUpdateDate(dest_path):
    last_update_date = None
    
    try:
        date_filename = "lastUpdateDate.txt"
        
        if dest_path == "c:\\Users\stanl.STANLEY\OneDrive":
            dest_path = dest_path + "\Documents"
        filename = path.join(dest_path, date_filename)
        f = open(filename, "r")
        last_update_date = dt.strptime(f.read(), "%d/%m/%Y").strftime("%Y/%m/%d")
        f.close()
        
        if last_update_date == "":
            last_update_date = "2021/01/01"
    except Exception as e:
        #print("[GetLastUpdateDate] occurred an error. last_update_date: " + last_update_date + ". ", e)
        WriteLog("[GetLastUpdateDate] occurred an error[" + last_update_date + "]: " + str(e))
        Toast("[GetLastUpdateDate] occurred an error[" + last_update_date + "]: " + str(e))

    return last_update_date

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
        #print("[UpdateLastUpdateDate] occurred an error. last_update_date: " + update_date + ". ")
        WriteLog("[UpdateLastUpdateDate] occurred an error[" + last_update_date + "]: " + str(e))
        Toast("[UpdateLastUpdateDate] occurred an error. last_update_date[" + last_update_date + "]: " + str(e))

syn = r"\\Hungs\stanley\Stanley"
dest1 = "c:\\Users\stanl.STANLEY\OneDrive"
dest2 = "C:\\Users\stanl.STANLEY\Documents"

Toast("Updating...")

for  in :

if path.exists(syn) and path.exists(dest1):
    lastUpdateDate = GetLastUpdateDate(dest1)
    UpdateFile(syn, dest1, lastUpdateDate)
    UpdateLastUpdateDate(dest1)
else:
    print(syn + " or " + dest1 + " is not found.")
    WriteLog(syn + " or " + dest1 + " is not found.")
    Toast(syn + " or " + dest1 + " is not found.")

if path.exists(syn) and path.exists(dest2):
    lastUpdateDate = GetLastUpdateDate(dest2)
    UpdateFile(syn, dest2, lastUpdateDate)
    UpdateLastUpdateDate(dest2)
else:
    print(syn + " or " + dest2 + " is not found.")
    WriteLog(syn + " or " + dest2 + " is not found.")
    Toast(syn + " or " + dest2 + " is not found.")

Toast("Update Complete. Please see log for more details.")
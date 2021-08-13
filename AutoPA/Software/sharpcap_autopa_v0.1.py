import glob
import os
import win32file
import re
import time
from datetime import datetime
import win32com.client

def getLatestSharpcapLog():
    list_of_files = glob.glob(f"{os.getenv('LOCALAPPDATA')}\SharpCap\logs\*.log") # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    f = win32file.CreateFile(latest_file, win32file.GENERIC_READ, win32file.FILE_SHARE_DELETE | win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
    bufSize = 4096
    code, data = win32file.ReadFile(f, bufSize)
    buf = data
    while len(data) == bufSize:
        result, data = win32file.ReadFile(f, bufSize, None)
        buf += data
    result = re.findall("(?:Info:)\t(\d{2}:\d{2}:\d{2}.\d{7}).*(?:AltAzCor=)(?:Alt=)(.*)[,](?:Az=)(.*).\s(?:AltAzPole=)(?:Alt=)(.*)[,](?:Az=)(.*).[,]\s(?:AltAzOffset=).*", buf.decode("utf-8"))[-1]
    return(result)

def altitudeError(error, pole):
    return(dmsTodeg(pole)-dmsTodeg(error))

def azimuthError(error, pole):
    return(((dmsTodeg(pole) + 180) % 360 - 180)-((dmsTodeg(error) + 180) % 360 - 180))

def dmsTodeg(input):
    temp = input.split(':')
    d = float(temp[0])
    m = float(temp[1]) / 60
    s = float(temp[2]) / 3600
    return (d + m + s)

def degToArcmin(input):
    return(input * 60)
    
def sendCommand(command):
    tel = win32com.client.Dispatch("ASCOM.OpenAstroTracker.Telescope")
    if tel.Connected:
        print("Telescope was already connected")
    else:
        tel.Connected = True
        if not tel.Connected:
            print("Unable to connect to telescope, expect exception")
    result = tel.Action("Serial:PassThroughCommand", command)
    tel.Connected = False
    return result

def isAdjusting():
    try:
        result = sendCommand(":GX#,#")
        print(result)
        status = re.search(",(......),", result)[1]
        if status[3]=="-" and status[4]=="-":
            return False
        else:
            return True
    except Exception as e:
        print("Problem determining mount status. Verify ASCOM/mount is connected.")

print("Starting AutoPA routine")

lastEntry = None
aligned = False
while aligned == False:
    if not isAdjusting():
        print("Getting latest log entry from Sharpcap.")
        try:
            log = getLatestSharpcapLog()
        except:
            log = None
        if log is not None:
            currentEntry = datetime.strptime(datetime.today().strftime("%Y-%m-%d") + " " + log[0][:-1], '%Y-%m-%d %H:%M:%S.%f') #get last log entry (assume todays date)
            if currentEntry != lastEntry:
                error = []
                error.append(degToArcmin(altitudeError(log[1], log[3])))
                print(f"Altitude error in arcminutes: {error[0]:.3f}\'")
                error.append(degToArcmin(azimuthError(log[2], log[4])))
                print(f"Azimuth error in arcminutes: {error[1]:.3f}\'")
                if abs(error[0]) < 1 and abs(error[1]) < 1:
                    aligned = True
                    break
                else:
                    print("Correction needed.")
                    if abs(error[0]) >= 1:
                        result = sendCommand(f":MAL{error[0]*(-1)}#")
                        #print(f"Adjusting altitude by {error[0]:.3f} arcminutes.")
                    if abs(error[1]) >= 1:
                        result = sendCommand(f":MAZ{error[1]}#")
                        #print(f"Adjusting azimuth by {error[1]:.3f} arcminutes.")
                    lastEntry = currentEntry
                    
            else:
                print("Waiting for Sharpcap to re-solve since last adjustment.")
        else:
            print("Sharpcap has not yet determined the polar alignment error.")
    else:
        print("Mount is still adjusting position.")
    time.sleep(5)
        
print(f"Polar aligned to within {error[0]*60:.0f}\" altitude and {error[1]*60:.0f}\" azimuth.")
exit()


















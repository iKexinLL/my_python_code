
import os 
import wmi

SoftName = 'WD Unlocker'
theSoftPath = ''
theSoftName = 'WD Drive Unlock.exe'
DiskName = 'My Passport'


wmiServer = wmi.WMI()

LogicalDisk = wmiServer.Win32_LogicalDisk()

# VolumeName

for ld in LogicalDisk:
    
    if ld.VolumeName == SoftName:
        theSoftPath = ld.Caption + '\\' + theSoftName
        os.system('"' + theSoftPath + '"')
        break
        

import os 
import wmi

DiskName = 'WD Unlocker'
theSoftPath = ''
theSoftName = 'WD Drive Unlock.exe'


wmiServer = wmi.WMI()

LogicalDisk = wmiServer.Win32_LogicalDisk()

# VolumeName

for ld in LogicalDisk:
    if ld.VolumeName == DiskName:
        theSoftPath = ld.Caption + '\\' + theSoftName
        os.system('"' + theSoftPath + '"')
        break
        
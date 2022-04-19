import sys,platform
from cx_Freeze import setup, Executable

def getTargetName():
    myOS = platform.system()
    if myOS == 'Linux':
        return "AutoPA_v2.1.0"
    elif myOS == 'Windows':
        return "AutoPA_v2.1.0.exe"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "AutoPA" ,
      version = "2.1.0" ,
      description = "" ,
      executables = [Executable(script = "autopa_v2.1.0.py", base=base, targetName = getTargetName())])
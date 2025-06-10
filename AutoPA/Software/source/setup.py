import sys, platform
from cx_Freeze import setup, Executable

def getTargetName():
    myOS = platform.system()
    if myOS == 'Linux':
        return "AutoPA_v2.3.0"
    elif myOS == 'Windows':
        return "AutoPA_v2.3.0.exe"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="AutoPA",
    version="2.3.0",
    description="AutoPA Polar Alignment Tool",
    executables=[
        Executable(
            script="autopa_v2.py",
            base=base,
            target_name=getTargetName(),
            icon=None  # Add icon path here if you have one
        )
    ],
    options={
        "build_exe": {
            "packages": ["os", "sys", "platform"],
            "include_files": []
        }
    }
)
import sys, platform
from cx_Freeze import setup, Executable

def getTargetName():
    myOS = platform.system()
    if myOS == 'Linux':
        return "AutoPA_v2.6.0"
    elif myOS == 'Windows':
        return "AutoPA_v2.6.0.exe"

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# List of required packages
packages = [
    "os", 
    "sys", 
    "platform",
    "glob",
    "re",
    "datetime",
    "json",
    "math",
    "PyQt5",
    "collections",
    "logging",
    "pathlib",
    "win32com.client",
    "serial",
    "indi"
]

# List of required files
include_files = []

setup(
    name="AutoPA",
    version="2.6.0",
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
            "packages": packages,
            "include_files": include_files,
            "excludes": ["tkinter", "unittest"],
            "include_msvcr": True,  # Include Microsoft Visual C++ Runtime
            "build_exe": "build/exe.win-amd64-3.7",  # Specify exact build directory
            "optimize": 2,  # Optimize bytecode
            "zip_include_packages": [],  # Don't zip any packages
            "zip_exclude_packages": ["*"],  # Exclude all packages from zipping
        }
    }
)
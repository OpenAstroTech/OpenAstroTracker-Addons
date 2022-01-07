from cx_Freeze import setup, Executable

setup(name = "AutoPA" ,
      version = "2.1.0" ,
      description = "" ,
      executables = [Executable("autopa_v2.1.0.py", base = "Win32GUI")])
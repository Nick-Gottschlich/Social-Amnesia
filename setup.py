from cx_Freeze import setup, Executable
from multiprocessing import Queue
import os
import sys

base = None
if sys.platform == "win32":
  base = "Win32GUI"
  os.environ['TCL_LIBRARY'] = "C:\\Python36\\tcl\\tcl8.6"
  os.environ['TK_LIBRARY'] = "C:\\Python36\\tcl\\tk8.6"
build_exe_options = {"packages": ["os", "idna"]}
setup(name="Social Amnesia",
      version="0.1.0",
      description="Social Amnesia",
      options={"build_exe": build_exe_options},
      executables=[Executable("SocialAmnesia.py", base=base)])

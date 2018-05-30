from cx_Freeze import setup, Executable
from multiprocessing import Queue
import os
import sys

base = None
if sys.platform == "win32":
  base = "Win32GUI"
build_exe_options = {"packages": ["os", "idna"]}
setup(name="Social Amnesia",
      version="0.0.1",
      description="Social Amnesia",
      options={"build_exe": build_exe_options},
      executables=[Executable("SocialAmnesia.py", base=base)])

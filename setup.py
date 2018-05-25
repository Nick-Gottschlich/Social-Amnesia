from cx_Freeze import setup, Executable
from multiprocessing import Queue
import os
import sys

base = None
if sys.platform == "win32":
  base = "Win32GUI"
build_exe_options = {"packages": ["os", "idna"]}
setup(name="Social Scrubber",
      version="0.1",
      description="Social Scrubber",
      options={"build_exe": build_exe_options},
      executables=[Executable("SocialScrubber.py", base=base)])

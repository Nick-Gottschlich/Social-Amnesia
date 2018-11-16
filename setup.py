import os
import sys

from cx_Freeze import setup, Executable

app_name = "Social Amnesia"
app_description = 'Forget the past. Social Amnesia makes sure ' \
                  'your social media accounts only show your posts ' \
                  'from recent history, not from "that phase" 5 years ago.'

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    os.environ['TCL_LIBRARY'] = 'C:\\Python36\\tcl\\tcl8.6'
    os.environ['TK_LIBRARY'] = 'C:\\Python36\\tcl\\tk8.6'

build_exe_options = {'packages': ['os', 'idna', 'multiprocessing', 'dbm']}
executables = [Executable('social_amnesia.py', base=base)]

setup(name=app_name,
      version='0.3.0',
      description=app_description,
      options={'build_exe': build_exe_options},
      executables=executables)

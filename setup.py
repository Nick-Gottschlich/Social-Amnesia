import os
import sys

from cx_Freeze import setup, Executable

app_name = "Social Amnesia"
app_description = 'Forget the past. Social Amnesia makes sure ' \
                  'your social media accounts only show your posts ' \
                  'from recent history, not from "that phase" 5 years ago.'

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    os.environ['TCL_LIBRARY'] = 'C:\\Python36\\tcl\\tcl8.6'
    os.environ['TK_LIBRARY'] = 'C:\\Python36\\tcl\\tk8.6'

build_exe_options = {'packages': ['os', 'idna', 'multiprocessing', 'dbm']}
bdist_mac_options = {'iconfile': find_data_file('icon.icns')}
executables = [Executable('SocialAmnesia.py', base=base, icon='icon.png')]

setup(name=app_name,
      version='1.0.0',
      description=app_description,
      options={'build_exe': build_exe_options, 'bdist_mac': bdist_mac_options},
      executables=executables)

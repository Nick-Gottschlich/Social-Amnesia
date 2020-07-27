#!/bin/sh

echo 'Building macOS executable...'
python3 setup.py bdist_dmg
echo 'Done! Check the build folder'
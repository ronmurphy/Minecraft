@echo off
@echo Attempting to start the World_Server...
c:\python\python.exe server.py --seed %1
@echo Server stopping.
cleanup.bat
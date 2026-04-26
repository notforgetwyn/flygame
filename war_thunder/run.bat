@echo off
powershell -Command "Start-Process -FilePath 'D:\py_3.11\python.exe' -ArgumentList '-m src.app' -WorkingDirectory '%CD%'"

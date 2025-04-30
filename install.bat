@echo off
call python -m venv venv
call venv\Scripts\activate
call pip install -r requirements.txt
xcopy input_example input /E /I /Y

echo Installation complete! 
pause

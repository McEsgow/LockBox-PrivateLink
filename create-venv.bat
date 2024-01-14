@echo off
echo Creating venv...
python -m venv venv
echo ____________________
echo Activating venv...
call .\venv\Scripts\activate
echo ____________________
echo Installing requirements...
python -m pip install -r requirements.txt
echo ____________________
echo Installation comlete! 
echo Thank you for installing LockBox-PrivateLink
echo ____________________
pause
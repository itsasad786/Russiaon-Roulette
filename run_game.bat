@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo ===============================================
echo    RUSSIAN ROULETTE - SYSTEM DESTROYER
echo ===============================================
echo.
echo WARNING: This game will actually crash your system!
echo Make sure you save all your work before playing!
echo.
echo Press any key to start the game...
pause >nul

python russian_roulette.py

pause

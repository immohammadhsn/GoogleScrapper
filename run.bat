@echo off
echo Installing packages...
pip install -r requirements.txt

echo running google scrapper
python ./Gsc.py
pause

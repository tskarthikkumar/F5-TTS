@echo off

:: Activate the Conda environment
call conda activate f5-tts

:: Run the Python script
python ./src/f5_tts/tsk_api.py

:: Deactivate the Conda environment
call conda deactivate

pause

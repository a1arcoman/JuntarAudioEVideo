@echo off
echo Gerando executavel do Video Audio Merger...
echo.

pyinstaller --onefile --windowed --name="VideoAudioMerger" video_audio_merger.py

echo.
echo Executavel gerado em: dist\VideoAudioMerger.exe
echo.
pause
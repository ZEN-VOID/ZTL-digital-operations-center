@echo off
chcp 65001 > nul
cd /d "%~dp0"
python export_figma_svg.py
pause

@echo off
for /f "delims=" %%a in (.env) do set ###%%a
for /f "tokens=2 delims==" %%a in ('set ###') do echo %%a

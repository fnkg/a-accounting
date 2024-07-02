@echo off
chcp 65001
cls
title СОЗДАВАТЕЛЬ ПАПОК
color 0a

:: Get the current date and time
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"

echo Оууее, давай-ка я создам тебе папки, красавчик!
echo Введи номер месяца (01-12):
set /p MM=
if "%MM%"=="" goto :eof

:: Map month numbers to month names
set "monthName=InvalidMonth"
if "%MM%"=="01" set "monthName=january"
if "%MM%"=="02" set "monthName=february"
if "%MM%"=="03" set "monthName=march"
if "%MM%"=="04" set "monthName=april"
if "%MM%"=="05" set "monthName=may"
if "%MM%"=="06" set "monthName=june"
if "%MM%"=="07" set "monthName=july"
if "%MM%"=="08" set "monthName=august"
if "%MM%"=="09" set "monthName=september"
if "%MM%"=="10" set "monthName=october"
if "%MM%"=="11" set "monthName=november"
if "%MM%"=="12" set "monthName=december"

set "parentFolder=%YY%-%MM%_%monthName%"
echo ваааау! %parentFolder% звучит круто.
md "%parentFolder%"
md "%parentFolder%\".readable""
md "%parentFolder%\card+cash"
md "%parentFolder%\realisations"
md "%parentFolder%\sbp"
echo кайфуй с кайфом!
pause
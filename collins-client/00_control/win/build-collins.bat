echo Building collins Windows
cd c:\Users\baerb\src\rubyinstaller
call rake clean
call rake ruby20
copy profile sandbox\devkit\etc
call sandbox\devkit\msys.bat
timeout 10
@echo off
:LOOP
TASKLIST | find /I "sh.exe" >nul 2>$1
  IF ERRORLEVEL 1 (
  GOTO CONTINUE
) ELSE (
	ECHO WAITING FOR MSYS ENVIRONMENT TO COMPLETE RUBY GEMS BUILD
	timeout 5
	GOTO LOOP
)

:CONTINUE
call "c:\Program Files (x86)\Inno Setup 5\ISCC.exe" /o"c:\Users\baerb\src\collins-installer" "c:\Program Files (x86)\Inno Setup 5\collinswindows.iss"
echo Collins Windows successfully built

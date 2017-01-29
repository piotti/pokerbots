@echo off
setlocal enabledelayedexpansion


for /l %%x in (1, 1, 40)  do (
	set /a num1 = %%x
	set /a num1 = !num1! %% 2
	set /a num2 = !num1! + 1
	echo !num1!, !num2!
	pause
	start runengine.bat
	start runtunebot.bat 3000 !num1!
	pause
	python Player.py 3001 !num2!
	pause
	python bottuner.py %%x
	python evolution.py
	pause
)
del winners.txt

